"""
Advanced Knowledge Base Management System for Ali 2025 Campaign Bot
Handles retrieval, search/matching logic, data structure, and source attribution
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import re
import hashlib
from collections import defaultdict
import sqlite3
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentType(Enum):
    POLICY = "policy"
    BIOGRAPHY = "biography"
    SPEECH = "speech"
    VOTING_RECORD = "voting_record"
    POSITION_STATEMENT = "position_statement"
    FAQ = "faq"
    NEWS_ARTICLE = "news_article"
    CAMPAIGN_EVENT = "campaign_event"
    ENDORSEMENT = "endorsement"

class SourceCredibility(Enum):
    PRIMARY = "primary"  # Official campaign sources
    VERIFIED = "verified"  # Trusted news sources, government records
    SECONDARY = "secondary"  # Other reputable sources
    UNVERIFIED = "unverified"  # Social media, unverified claims

@dataclass
class KnowledgeSource:
    """Represents a source of information with credibility tracking"""
    url: str
    title: str
    source_type: str  # website, document, speech, etc.
    credibility: SourceCredibility
    date_published: Optional[datetime] = None
    author: Optional[str] = None
    language: str = "en"
    
    def to_dict(self) -> Dict:
        return {
            'url': self.url,
            'title': self.title,
            'source_type': self.source_type,
            'credibility': self.credibility.value,
            'date_published': self.date_published.isoformat() if self.date_published else None,
            'author': self.author,
            'language': self.language
        }

@dataclass
class KnowledgeItem:
    """Represents a piece of knowledge with rich metadata"""
    id: str
    content: str
    content_type: ContentType
    topic: str
    subtopic: Optional[str] = None
    keywords: List[str] = None
    sources: List[KnowledgeSource] = None
    confidence_score: float = 1.0
    language: str = "en"
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.sources is None:
            self.sources = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content,
            'content_type': self.content_type.value,
            'topic': self.topic,
            'subtopic': self.subtopic,
            'keywords': self.keywords,
            'sources': [source.to_dict() for source in self.sources],
            'confidence_score': self.confidence_score,
            'language': self.language,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class KnowledgeBaseManager:
    """
    Advanced Knowledge Base Management System
    """
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = db_path
        self.init_database()
        
        # Multilingual keyword mappings
        self.multilingual_keywords = self._load_multilingual_keywords()
        
        # Topic hierarchies for better matching
        self.topic_hierarchy = self._build_topic_hierarchy()
        
        logger.info(f"Knowledge Base Manager initialized with database: {db_path}")
    
    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize the SQLite database with proper schema"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Knowledge items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    subtopic TEXT,
                    keywords TEXT,  -- JSON array
                    confidence_score REAL DEFAULT 1.0,
                    language TEXT DEFAULT 'en',
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            ''')
            
            # Sources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    knowledge_item_id TEXT,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    credibility TEXT NOT NULL,
                    date_published TIMESTAMP,
                    author TEXT,
                    language TEXT DEFAULT 'en',
                    FOREIGN KEY (knowledge_item_id) REFERENCES knowledge_items (id)
                )
            ''')
            
            # Full-text search index
            cursor.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
                    id UNINDEXED,
                    content,
                    topic,
                    subtopic,
                    keywords
                )
            ''')
            
            # Create indices for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_topic ON knowledge_items(topic)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_language ON knowledge_items(language)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_content_type ON knowledge_items(content_type)')
            
            conn.commit()
    
    def _load_multilingual_keywords(self) -> Dict[str, Dict[str, List[str]]]:
        """Load multilingual keyword mappings"""
        return {
            "education": {
                "en": ["education", "schools", "teachers", "students", "learning", "graduation", "classroom"],
                "es": ["educación", "escuelas", "maestros", "estudiantes", "aprendizaje", "graduación", "aula"],
                "ar": ["التعليم", "المدارس", "المعلمين", "الطلاب", "التعلم", "التخرج", "الفصول الدراسية"],
                "fr": ["éducation", "écoles", "enseignants", "étudiants", "apprentissage", "diplômation", "salle de classe"]
            },
            "housing": {
                "en": ["housing", "rent", "affordable", "apartments", "homes", "real estate", "landlord"],
                "es": ["vivienda", "alquiler", "asequible", "apartamentos", "casas", "bienes raíces", "propietario"],
                "ar": ["الإسكان", "الإيجار", "ميسور التكلفة", "الشقق", "المنازل", "العقارات", "المالك"],
                "fr": ["logement", "loyer", "abordable", "appartements", "maisons", "immobilier", "propriétaire"]
            },
            "transportation": {
                "en": ["transportation", "transit", "buses", "trains", "traffic", "roads", "public transport"],
                "es": ["transporte", "tránsito", "autobuses", "trenes", "tráfico", "carreteras", "transporte público"],
                "ar": ["النقل", "المواصلات", "الحافلات", "القطارات", "المرور", "الطرق", "النقل العام"],
                "fr": ["transport", "transit", "autobus", "trains", "circulation", "routes", "transport public"]
            },
            "safety": {
                "en": ["safety", "crime", "police", "security", "violence", "law enforcement"],
                "es": ["seguridad", "crimen", "policía", "seguridad", "violencia", "aplicación de la ley"],
                "ar": ["الأمان", "الجريمة", "الشرطة", "الأمن", "العنف", "إنفاذ القانون"],
                "fr": ["sécurité", "crime", "police", "sécurité", "violence", "application de la loi"]
            },
            "economy": {
                "en": ["economy", "jobs", "employment", "wages", "business", "taxes", "budget"],
                "es": ["economía", "empleos", "empleo", "salarios", "negocios", "impuestos", "presupuesto"],
                "ar": ["الاقتصاد", "الوظائف", "التوظيف", "الأجور", "الأعمال", "الضرائب", "الميزانية"],
                "fr": ["économie", "emplois", "emploi", "salaires", "entreprises", "taxes", "budget"]
            }
        }
    
    def _build_topic_hierarchy(self) -> Dict[str, List[str]]:
        """Build hierarchical topic relationships"""
        return {
            "education": ["school_budget", "teacher_pay", "graduation_rates", "school_safety", "curriculum"],
            "housing": ["affordable_housing", "rent_control", "zoning", "development", "homelessness"],
            "transportation": ["bus_service", "bike_lanes", "traffic", "parking", "congestion_pricing"],
            "public_safety": ["police_reform", "crime_prevention", "community_policing", "emergency_services"],
            "economy": ["job_creation", "small_business", "taxation", "budget", "development"],
            "environment": ["climate_change", "green_energy", "sustainability", "pollution", "parks"],
            "healthcare": ["public_health", "mental_health", "healthcare_access", "insurance"],
            "governance": ["transparency", "accountability", "ethics", "civic_engagement"]
        }
    
    def add_knowledge_item(self, item: KnowledgeItem) -> bool:
        """Add a knowledge item to the database"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Insert knowledge item
                cursor.execute('''
                    INSERT OR REPLACE INTO knowledge_items 
                    (id, content, content_type, topic, subtopic, keywords, confidence_score, language, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.id, item.content, item.content_type.value, item.topic, item.subtopic,
                    json.dumps(item.keywords), item.confidence_score, item.language,
                    item.created_at.isoformat(), item.updated_at.isoformat()
                ))
                
                # Delete existing sources for this item
                cursor.execute('DELETE FROM sources WHERE knowledge_item_id = ?', (item.id,))
                
                # Insert sources
                for source in item.sources:
                    cursor.execute('''
                        INSERT INTO sources 
                        (knowledge_item_id, url, title, source_type, credibility, date_published, author, language)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item.id, source.url, source.title, source.source_type, source.credibility.value,
                        source.date_published.isoformat() if source.date_published else None,
                        source.author, source.language
                    ))
                
                # Update FTS index
                cursor.execute('''
                    INSERT OR REPLACE INTO knowledge_fts (id, content, topic, subtopic, keywords)
                    VALUES (?, ?, ?, ?, ?)
                ''', (item.id, item.content, item.topic, item.subtopic, ' '.join(item.keywords)))
                
                conn.commit()
                logger.info(f"Added knowledge item: {item.id}")
                return True
                
        except Exception as e:
            logger.error(f"Error adding knowledge item {item.id}: {str(e)}")
            return False
    
    def search_knowledge(self, query: str, language: str = "en", limit: int = 10) -> List[Tuple[KnowledgeItem, float]]:
        """
        Advanced search with multilingual support and relevance scoring
        """
        results = []
        
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Normalize query
                normalized_query = self._normalize_query(query, language)
                
                # Multi-stage search approach
                
                # 1. Exact keyword matches (highest priority)
                exact_matches = self._search_exact_keywords(cursor, normalized_query, language)
                results.extend([(item, score * 1.0) for item, score in exact_matches])
                
                # 2. FTS search
                fts_matches = self._search_fts(cursor, normalized_query, language)
                results.extend([(item, score * 0.8) for item, score in fts_matches])
                
                # 3. Semantic similarity (topic-based)
                topic_matches = self._search_by_topic(cursor, normalized_query, language)
                results.extend([(item, score * 0.6) for item, score in topic_matches])
                
                # 4. Multilingual keyword expansion
                if language != "en":
                    expanded_matches = self._search_multilingual_expansion(cursor, query, language)
                    results.extend([(item, score * 0.7) for item, score in expanded_matches])
                
                # Remove duplicates and sort by score
                unique_results = {}
                for item, score in results:
                    if item.id not in unique_results or unique_results[item.id][1] < score:
                        unique_results[item.id] = (item, score)
                
                # Sort by relevance score and limit results
                sorted_results = sorted(unique_results.values(), key=lambda x: x[1], reverse=True)
                return sorted_results[:limit]
                
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return []
    
    def _normalize_query(self, query: str, language: str) -> str:
        """Normalize query for better matching"""
        query = query.lower().strip()
        
        # Remove common stop words
        stop_words = {
            "en": ["the", "is", "are", "was", "were", "will", "would", "should", "could"],
            "es": ["el", "la", "los", "las", "es", "son", "fue", "fueron", "será"],
            "ar": ["في", "من", "إلى", "على", "هو", "هي", "كان", "كانت"],
            "fr": ["le", "la", "les", "est", "sont", "était", "étaient", "sera"]
        }
        
        words = query.split()
        filtered_words = [w for w in words if w not in stop_words.get(language, [])]
        return " ".join(filtered_words)
    
    def _search_exact_keywords(self, cursor, query: str, language: str) -> List[Tuple[KnowledgeItem, float]]:
        """Search for exact keyword matches"""
        results = []
        query_words = set(query.split())
        
        cursor.execute('''
            SELECT * FROM knowledge_items 
            WHERE language = ? OR language = 'en'
            ORDER BY confidence_score DESC
        ''', (language,))
        
        for row in cursor.fetchall():
            item = self._row_to_knowledge_item(dict(row), cursor)
            item_keywords = set(item.keywords)
            
            # Calculate keyword overlap
            overlap = len(query_words.intersection(item_keywords))
            if overlap > 0:
                score = overlap / max(len(query_words), len(item_keywords))
                results.append((item, score))
        
        return results
    
    def _search_fts(self, cursor, query: str, language: str) -> List[Tuple[KnowledgeItem, float]]:
        """Full-text search using SQLite FTS"""
        results = []
        
        try:
            # Clean and prepare FTS query - escape special characters
            clean_words = []
            for word in query.split():
                # Remove special FTS characters that cause syntax errors
                clean_word = ''.join(c for c in word if c.isalnum())
                if clean_word:
                    clean_words.append(f'"{clean_word}"')  # Use phrase search
            
            if not clean_words:
                return results
            
            fts_query = " OR ".join(clean_words)
            
            cursor.execute('''
                SELECT ki.*, -1 as rank
                FROM knowledge_fts kf
                JOIN knowledge_items ki ON kf.id = ki.id
                WHERE knowledge_fts MATCH ?
                AND (ki.language = ? OR ki.language = 'en')
                LIMIT 10
            ''', (fts_query, language))
            
            for row in cursor.fetchall():
                item = self._row_to_knowledge_item(dict(row), cursor)
                # Simple scoring for FTS results
                score = 0.7
                results.append((item, score))
                
        except Exception as e:
            logger.warning(f"FTS search failed: {e}")
            # Fall back to simple content search
            return self._fallback_content_search(cursor, query, language)
        
        return results
    
    def _fallback_content_search(self, cursor, query: str, language: str) -> List[Tuple[KnowledgeItem, float]]:
        """Fallback content search using LIKE"""
        results = []
        query_words = query.split()
        
        for word in query_words[:3]:  # Limit to first 3 words
            if len(word) > 2:  # Skip very short words
                cursor.execute('''
                    SELECT * FROM knowledge_items 
                    WHERE (content LIKE ? OR keywords LIKE ?)
                    AND (language = ? OR language = 'en')
                    ORDER BY confidence_score DESC
                    LIMIT 5
                ''', (f'%{word}%', f'%{word}%', language))
                
                for row in cursor.fetchall():
                    item = self._row_to_knowledge_item(dict(row), cursor)
                    score = 0.4  # Lower score for fallback search
                    results.append((item, score))
        
        return results
    
    def _search_by_topic(self, cursor, query: str, language: str) -> List[Tuple[KnowledgeItem, float]]:
        """Search by topic hierarchy"""
        results = []
        query_lower = query.lower()
        
        # Find relevant topics
        relevant_topics = []
        for topic, subtopics in self.topic_hierarchy.items():
            if topic.lower() in query_lower:
                relevant_topics.append(topic)
            for subtopic in subtopics:
                if subtopic.lower().replace("_", " ") in query_lower:
                    relevant_topics.append(topic)
        
        if relevant_topics:
            placeholders = ",".join("?" * len(relevant_topics))
            cursor.execute(f'''
                SELECT * FROM knowledge_items 
                WHERE topic IN ({placeholders})
                AND (language = ? OR language = 'en')
                ORDER BY confidence_score DESC
            ''', relevant_topics + [language])
            
            for row in cursor.fetchall():
                item = self._row_to_knowledge_item(dict(row), cursor)
                # Score based on topic relevance
                score = 0.5 if item.topic in relevant_topics else 0.3
                results.append((item, score))
        
        return results
    
    def _search_multilingual_expansion(self, cursor, query: str, language: str) -> List[Tuple[KnowledgeItem, float]]:
        """Expand search using multilingual keyword mappings"""
        results = []
        expanded_keywords = set()
        
        # Find English equivalents of non-English query terms
        for topic, translations in self.multilingual_keywords.items():
            if language in translations:
                for word in query.split():
                    if word.lower() in [k.lower() for k in translations[language]]:
                        expanded_keywords.update(translations["en"])
        
        if expanded_keywords:
            # Search with expanded English keywords
            expanded_query = " ".join(expanded_keywords)
            return self._search_exact_keywords(cursor, expanded_query, "en")
        
        return results
    
    def _row_to_knowledge_item(self, row_dict: Dict, cursor) -> KnowledgeItem:
        """Convert database row to KnowledgeItem object"""
        
        # Get sources for this item
        cursor.execute('SELECT * FROM sources WHERE knowledge_item_id = ?', (row_dict['id'],))
        source_rows = cursor.fetchall()
        
        sources = []
        for source_row in source_rows:
            source_dict = dict(source_row)
            sources.append(KnowledgeSource(
                url=source_dict['url'],
                title=source_dict['title'],
                source_type=source_dict['source_type'],
                credibility=SourceCredibility(source_dict['credibility']),
                date_published=datetime.fromisoformat(source_dict['date_published']) if source_dict['date_published'] else None,
                author=source_dict['author'],
                language=source_dict['language']
            ))
        
        return KnowledgeItem(
            id=row_dict['id'],
            content=row_dict['content'],
            content_type=ContentType(row_dict['content_type']),
            topic=row_dict['topic'],
            subtopic=row_dict['subtopic'],
            keywords=json.loads(row_dict['keywords']),
            sources=sources,
            confidence_score=row_dict['confidence_score'],
            language=row_dict['language'],
            created_at=datetime.fromisoformat(row_dict['created_at']),
            updated_at=datetime.fromisoformat(row_dict['updated_at'])
        )
    
    def get_item_by_id(self, item_id: str) -> Optional[KnowledgeItem]:
        """Retrieve a specific knowledge item by ID"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM knowledge_items WHERE id = ?', (item_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_knowledge_item(dict(row), cursor)
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving knowledge item {item_id}: {str(e)}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Total items
                cursor.execute('SELECT COUNT(*) FROM knowledge_items')
                stats['total_items'] = cursor.fetchone()[0]
                
                # Items by content type
                cursor.execute('''
                    SELECT content_type, COUNT(*) 
                    FROM knowledge_items 
                    GROUP BY content_type
                ''')
                stats['by_content_type'] = dict(cursor.fetchall())
                
                # Items by language
                cursor.execute('''
                    SELECT language, COUNT(*) 
                    FROM knowledge_items 
                    GROUP BY language
                ''')
                stats['by_language'] = dict(cursor.fetchall())
                
                # Items by topic
                cursor.execute('''
                    SELECT topic, COUNT(*) 
                    FROM knowledge_items 
                    GROUP BY topic
                    ORDER BY COUNT(*) DESC
                    LIMIT 10
                ''')
                stats['top_topics'] = dict(cursor.fetchall())
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on character patterns"""
        # This is a basic implementation - in production, use a proper language detection library
        
        # Check for Arabic characters
        if re.search(r'[\u0600-\u06FF]', text):
            return 'ar'
        
        # Check for Spanish patterns (basic)
        spanish_patterns = ['ñ', 'ü', 'é', 'á', 'í', 'ó', 'ú']
        if any(pattern in text.lower() for pattern in spanish_patterns):
            return 'es'
        
        # Check for French patterns (basic)
        french_patterns = ['ç', 'à', 'è', 'ù', 'â', 'ê', 'î', 'ô', 'û']
        if any(pattern in text.lower() for pattern in french_patterns):
            return 'fr'
        
        # Default to English
        return 'en'


def create_sample_knowledge_base():
    """Create sample knowledge base entries for testing"""
    kb = KnowledgeBaseManager()
    
    # Sample FAQ data based on your campaign content
    sample_items = [
        {
            "id": "faq_experience",
            "content": "While Mussab is young (he's 28 and the only candidate running under 40), he is also ridiculously accomplished. After the Covid-19 pandemic, he went to Harvard Law School, beat cancer, was elected to the school board (the only mayoral candidate to hold city-wide office in Jersey City), and was then elected the youngest school board president in Jersey City history. He's young, but we think of that as a feature, not a bug for someone as accomplished as him!",
            "content_type": ContentType.FAQ,
            "topic": "candidate_qualifications",
            "keywords": ["experience", "young", "age", "Harvard", "school board", "president", "accomplished"],
            "language": "en"
        },
        {
            "id": "faq_taxes_school_budget",
            "content": "I totally get it—no one likes opening their tax bill and seeing a higher number. The reality is that when Mussab was school‑board president, Trenton cut more than $150 million in state aid to our schools. That left Jersey City kids getting thousands of dollars less per student than New Jersey itself says is adequate. Mussab faced a tough choice: either raise the local share a bit to keep teachers, counselors, and after‑school programs—or let class sizes explode and watch our property values drop.",
            "content_type": ContentType.FAQ,
            "topic": "education",
            "subtopic": "school_budget",
            "keywords": ["taxes", "budget", "school", "state aid", "Trenton", "teachers", "property values"],
            "language": "en"
        }
    ]
    
    for item_data in sample_items:
        sources = [KnowledgeSource(
            url="https://www.ali2025.com/",
            title="Ali 2025 Campaign",
            source_type="website",
            credibility=SourceCredibility.PRIMARY,
            language=item_data["language"]
        )]
        
        item = KnowledgeItem(
            id=item_data["id"],
            content=item_data["content"],
            content_type=item_data["content_type"],
            topic=item_data["topic"],
            subtopic=item_data.get("subtopic"),
            keywords=item_data["keywords"],
            sources=sources,
            language=item_data["language"]
        )
        
        kb.add_knowledge_item(item)
    
    logger.info("Sample knowledge base created successfully")
    return kb

if __name__ == "__main__":
    # Create and test the knowledge base
    kb = create_sample_knowledge_base()
    
    # Test search functionality
    test_queries = [
        "What experience does Mussab have?",
        "Why did taxes increase?",
        "school budget problems"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = kb.search_knowledge(query)
        for item, score in results[:3]:  # Top 3 results
            print(f"Score: {score:.3f} | Topic: {item.topic} | Content: {item.content[:100]}...")
    
    # Print statistics
    print(f"\nKnowledge Base Statistics:")
    stats = kb.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
