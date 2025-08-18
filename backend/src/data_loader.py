"""
Data Loader for Ali 2025 Campaign Knowledge Base
Imports policies, FAQs, speeches, voting records, and news articles
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import requests
from bs4 import BeautifulSoup

from knowledge_base import (
    KnowledgeBaseManager, KnowledgeItem, KnowledgeSource, 
    ContentType, SourceCredibility
)

logger = logging.getLogger(__name__)

class CampaignDataLoader:
    """Loads campaign data from various sources into the knowledge base"""
    
    def __init__(self, knowledge_base: KnowledgeBaseManager):
        self.kb = knowledge_base
    
    def load_comprehensive_faqs(self):
        """Load comprehensive FAQ data including your detailed responses"""
        
        faqs = [
            {
                "id": "faq_experience",
                "question": "Mussab doesn't have any experience – why should I vote for him?",
                "content": "While Mussab is young (he's 28 and the only candidate running under 40), he is also ridiculously accomplished. After the Covid-19 pandemic, he went to Harvard Law School, beat cancer, was elected to the school board (the only mayoral candidate to hold city-wide office in Jersey City), and was then elected the youngest school board president in Jersey City history. He's young, but we think of that as a feature, not a bug for someone as accomplished as him!",
                "topic": "candidate_qualifications",
                "keywords": ["experience", "young", "age", "Harvard", "school board", "president", "accomplished", "inexperienced", "qualify", "qualified", "too young"]
            },
            {
                "id": "faq_policies",
                "question": "Mussab just has talking points but no concrete policy proposals.",
                "content": "Check out our website! Mussab has a lot of great, detailed policy explanations for what he'd do in office. Everything from expanding bus service citywide to criminal justice reform in Jersey City. You will see detailed policies backed by data and a clear understanding of what matters to Jersey City residents.",
                "topic": "policy_platform",
                "keywords": ["talking points", "policy", "policies", "proposals", "concrete", "detailed", "plan", "plans"]
            },
            {
                "id": "faq_taxes_detailed",
                "question": "When he was president the school board budget increased which led to higher taxes, I don't like that!",
                "content": "I totally get it—no one likes opening their tax bill and seeing a higher number. The reality is that when Mussab was school‑board president, Trenton cut more than $150 million in state aid to our schools. That left Jersey City kids getting thousands of dollars less per student than New Jersey itself says is adequate. Mussab faced a tough choice: either raise the local share a bit to keep teachers, counselors, and after‑school programs—or let class sizes explode and watch our property values drop. He chose to protect our kids and our home equity, but he didn't write a blank check. He trimmed non‑essential spending, pushed for cost controls, and even sued the State to get our aid restored—no other trustee did that. And he's still holding the line: just this spring he called out a proposed 20% school‑tax hike as 'unacceptable,' proving he'll challenge waste even when he's not on the board. The payoff is real. Strong schools keep neighborhoods safe and property values high; a few hundred dollars now can safeguard tens of thousands in equity later. And as mayor, Mussab's plan goes further: enforce the payroll‑tax law so big corporations pay their fair share, pursue a vacancy tax on speculators, and launch a joint City Hall–BOE finance task force with public dashboards so every resident can see where each dollar goes. Mussab believes Jersey City shouldn't have to choose between great schools or affordable living. He's already shown he'll make the tough calls to protect both our kids and our wallets—that's exactly the balance we need in City Hall.",
                "topic": "education",
                "subtopic": "school_budget",
                "keywords": ["taxes", "budget", "increase", "higher", "expensive", "cost", "money", "school board", "state aid", "Trenton", "teachers", "property values"]
            },
            {
                "id": "faq_corruption",
                "question": "There is a lot of corruption on the school board, a group that Mussab is strongly affiliated with. I don't want more corruption in Jersey City.",
                "content": "Mussab was president of the school board during the pandemic, he went to law school and has been running for mayor during the current scandals. When Mussab was president, the school board was a reputable organization. He will institute that same reputability to the mayor's office when he wins this year.",
                "topic": "ethics",
                "keywords": ["corruption", "corrupt", "scandal", "ethics", "dishonest", "school board"]
            },
            {
                "id": "faq_serious_candidate",
                "question": "I haven't heard of him before – is Mussab a serious candidate?",
                "content": "Absolutely, Mussab is consistently one of the top fundraisers in the race, has had national figures such as Keith Ellison, Ilhan Omar, and Ro Khanna supporting his campaign and is the only candidate in this race who has successfully won an election for a city-wide office in Jersey City.",
                "topic": "candidate_viability",
                "keywords": ["serious", "haven't heard", "unknown", "candidate", "fundraising", "support", "Keith Ellison", "Ilhan Omar", "Ro Khanna"]
            },
            {
                "id": "faq_faith",
                "question": "Why is Mussab's faith so important to him? Why does he need to mention it as a part of his story?",
                "content": "Mussab's Islamic faith is a core part of who he is and he doesn't want to shy away from it. Of course, Mussab is running for a Jersey City for all, regardless of faith, color, or creed. That said, he doesn't want to hide who he is – his faith is a core reason he was called to public service when our incumbent President insulted Jersey City by lying and saying that people like Mussab's parents celebrated 9/11. Mussab runs for the dignity of all people to ensure bigots like our current president don't have the final say on our city.",
                "topic": "personal_background",
                "keywords": ["faith", "religion", "islamic", "muslim", "mention", "important", "9/11", "dignity"]
            },
            {
                "id": "faq_safety",
                "question": "Jersey City has gotten more dangerous over the years. What's Mussab going to do about that?",
                "content": "Mussab is going to continue to invest in our police department while holding them accountable. We need accountable law enforcement, not just a department with a blank check. Jersey City ranks among the lowest of New Jersey cities in police accountability when complaints are received. We need to stop this while ensuring that citizens feel safe. This isn't hard to do – it just requires leadership that demands accountability and results.",
                "topic": "public_safety",
                "keywords": ["dangerous", "safety", "crime", "police", "law enforcement", "security", "accountability"]
            },
            {
                "id": "faq_transit",
                "question": "Public transit is more expensive and worse quality than ever in Jersey City!",
                "content": "Mussab is adding bus lines and making city buses free for all. He is additionally going to demand a share of congestion pricing revenue to reinvest in our city.",
                "topic": "transportation",
                "keywords": ["transit", "bus", "transportation", "expensive", "quality", "public transport", "free buses", "congestion pricing"]
            },
            {
                "id": "faq_housing",
                "question": "I can't afford to buy a house in Jersey City anymore and rent is too expensive.",
                "content": "Mussab is committing to expand zoning to allow more residential construction and approve over 25,000 units to meet the demand of Jersey City residents. He also will ensure that all new buildings have affordable housing units, will cap rent increases by developers, and will prioritize Jersey City residents for affordable housing.",
                "topic": "housing",
                "keywords": ["housing", "rent", "afford", "expensive", "house", "apartment", "affordable", "zoning", "25000 units", "rent cap"]
            },
            {
                "id": "faq_jobs",
                "question": "It's hard to find a good job with a fair wage to afford to live in Jersey City anymore. How is Mussab going to improve that?",
                "content": "Mussab is committed to bringing high paying jobs to Jersey City and ensuring that residents get access to the best job training services possible. Mussab increased teacher pay significantly during his tenure as school board president and looks forward to doing the same for all Jersey City residents, while making Jersey City the best place to do business with policies such as permitting reform.",
                "topic": "economy",
                "subtopic": "job_creation",
                "keywords": ["jobs", "employment", "wage", "salary", "work", "career", "training", "high paying", "job training", "permitting reform"]
            },
            {
                "id": "faq_schools",
                "question": "I pay a lot to live in Jersey City and the public schools for my kids aren't very good. How is Mussab going to improve them?",
                "content": "Mussab was president of the school board so he understands better than anyone else running in this race what it takes to run our public schools and improve them. Graduation rates rose significantly during his tenure, he improved teacher pay, removed lead from drinking water, and provided prescription glasses to students free of charge.",
                "topic": "education",
                "subtopic": "school_quality",
                "keywords": ["schools", "education", "kids", "children", "students", "teachers", "learning", "graduation rates", "lead", "glasses"]
            },
            {
                "id": "faq_climate",
                "question": "What is Mussab going to do to combat climate change as Mayor of Jersey City?",
                "content": "Mussab is prioritizing public transit options (including free city-wide buses) and bike access infrastructure as Mayor to ensure that we continue to improve on the air quality and environmental friendliness of Jersey City.",
                "topic": "environment",
                "keywords": ["climate", "environment", "green", "sustainability", "carbon", "pollution", "bike infrastructure", "air quality"]
            },
            {
                "id": "faq_corruption_general",
                "question": "I'm sick of all the corruption in our city! How is Mussab going to change that?",
                "content": "Mussab is committed to ending pay-to-play politics. You don't get a seat at the table just because you donated to his campaign. We need to turn city contracts into a meritocracy. It reduces costs for Jersey City residents and ensures our community gets the best service.",
                "topic": "governance",
                "subtopic": "ethics_reform",
                "keywords": ["corruption", "pay-to-play", "contracts", "politics", "ethics", "transparency", "meritocracy"]
            }
        ]
        
        # Load FAQs into knowledge base
        for faq_data in faqs:
            source = KnowledgeSource(
                url="https://www.ali2025.com/",
                title="Ali 2025 Campaign FAQ",
                source_type="campaign_website",
                credibility=SourceCredibility.PRIMARY,
                language="en"
            )
            
            item = KnowledgeItem(
                id=faq_data["id"],
                content=faq_data["content"],
                content_type=ContentType.FAQ,
                topic=faq_data["topic"],
                subtopic=faq_data.get("subtopic"),
                keywords=faq_data["keywords"],
                sources=[source],
                confidence_score=1.0,
                language="en"
            )
            
            success = self.kb.add_knowledge_item(item)
            if success:
                logger.info(f"Loaded FAQ: {faq_data['id']}")
            else:
                logger.error(f"Failed to load FAQ: {faq_data['id']}")
    
    def load_news_articles(self):
        """Load news articles and external source information"""
        
        news_articles = [
            {
                "id": "jc_times_budget_2020",
                "title": "School Board Approves $736 Million Budget Proposal Representing a 47% Increase in the School Tax Levy",
                "content": "Jersey City Board of Education approved a $736 million budget proposal representing a 47% increase in the school tax levy. If approved, it would increase the school tax levy (the part of assessed property taxes allocated to the public schools) $64 million, bringing the levy to $201 million. The budget was necessary due to significant cuts in state aid.",
                "url": "https://jcitytimes.com/school-board-approves-736-million-budget-proposal-representing-a-47-increase-in-the-school-tax-levy/",
                "author": "Sally Deering",
                "date_published": "2020-03-23",
                "topic": "education",
                "subtopic": "school_budget",
                "keywords": ["school board", "budget", "tax levy", "47%", "increase", "$736 million", "state aid cuts"]
            },
            {
                "id": "hudson_view_ali_criticism_2025",
                "title": "Ali tees off on Jersey City BOE: 'This budget will result in a $90 million tax increase'",
                "content": "Jersey City mayoral candidate Mussab Ali is teeing off on the board of education's preliminary $1,027,273,122 budget with a roughly 20 percent tax increase, calling the spending plan 'unacceptable' since it 'will result in a $90 million tax increase.' This demonstrates Ali's continued fiscal watchdog role even after leaving the school board.",
                "url": "https://hudsoncountyview.com/ali-tees-off-on-jersey-city-boe-this-budget-will-result-in-a-90-million-tax-increase/",
                "author": "John Heinis",
                "date_published": "2025-03-24",
                "topic": "education",
                "subtopic": "fiscal_oversight",
                "keywords": ["Ali", "BOE", "budget", "20 percent", "tax increase", "$90 million", "unacceptable", "fiscal watchdog"]
            },
            {
                "id": "jc_times_joint_session_2021",
                "title": "Budget Crisis Solutions Discussed at Second Joint Session",
                "content": "Jersey City Board of Education and city council representatives met for the second time, with Board President Mussab Ali stating that school funding is the most important issue facing the city over the next three years. The meeting addressed ongoing budget crisis solutions.",
                "url": "https://jcitytimes.com/budget-crisis-solutions-discussed-at-second-joint-session/",
                "author": "Andrea Crowley-Hughes", 
                "date_published": "2021-05-06",
                "topic": "education",
                "subtopic": "funding_crisis",
                "keywords": ["Mussab Ali", "school funding", "most important issue", "budget crisis", "joint session", "board president"]
            }
        ]
        
        for article_data in news_articles:
            source = KnowledgeSource(
                url=article_data["url"],
                title=article_data["title"],
                source_type="news_article",
                credibility=SourceCredibility.VERIFIED,
                date_published=datetime.fromisoformat(article_data["date_published"]),
                author=article_data["author"],
                language="en"
            )
            
            item = KnowledgeItem(
                id=article_data["id"],
                content=article_data["content"],
                content_type=ContentType.NEWS_ARTICLE,
                topic=article_data["topic"],
                subtopic=article_data.get("subtopic"),
                keywords=article_data["keywords"],
                sources=[source],
                confidence_score=0.9,  # High confidence for verified news sources
                language="en"
            )
            
            success = self.kb.add_knowledge_item(item)
            if success:
                logger.info(f"Loaded news article: {article_data['id']}")
            else:
                logger.error(f"Failed to load news article: {article_data['id']}")
    
    def load_policy_positions(self):
        """Load detailed policy positions"""
        
        policies = [
            {
                "id": "policy_housing_comprehensive",
                "title": "Comprehensive Housing Policy",
                "content": "Mussab's housing policy includes expanding zoning to allow more residential construction, approving over 25,000 housing units to meet demand, ensuring all new buildings include affordable housing units, capping rent increases by developers, prioritizing Jersey City residents for affordable housing, and implementing a vacancy tax on speculators. The goal is to make Jersey City affordable for working families while maintaining neighborhood character.",
                "topic": "housing",
                "subtopic": "comprehensive_plan",
                "keywords": ["zoning expansion", "25000 units", "affordable housing", "rent cap", "vacancy tax", "working families", "neighborhood character"]
            },
            {
                "id": "policy_transportation_free_buses", 
                "title": "Free Public Transportation Initiative",
                "content": "Mussab proposes making all city buses completely free for residents, expanding bus routes citywide, improving frequency and reliability, and demanding Jersey City's fair share of congestion pricing revenue to reinvest in local transportation infrastructure. This policy aims to reduce car dependency, improve air quality, and make transportation accessible to all residents regardless of income.",
                "topic": "transportation",
                "subtopic": "free_transit",
                "keywords": ["free buses", "citywide routes", "congestion pricing", "car dependency", "air quality", "accessible transportation"]
            },
            {
                "id": "policy_police_accountability",
                "title": "Police Accountability and Reform",
                "content": "Mussab's public safety plan focuses on continuing investment in police while demanding accountability. Jersey City ranks among the lowest in New Jersey for police accountability when complaints are received. The plan includes transparent complaint processes, community oversight, data-driven policing strategies, and ensuring public safety while building community trust.",
                "topic": "public_safety",
                "subtopic": "police_reform",
                "keywords": ["police accountability", "community oversight", "transparent processes", "data-driven policing", "community trust", "public safety"]
            },
            {
                "id": "policy_ethics_reform",
                "title": "Ethics and Anti-Corruption Measures", 
                "content": "Mussab is committed to ending pay-to-play politics in Jersey City. His ethics platform includes turning city contracts into a merit-based system, creating public dashboards for budget transparency, establishing strict conflict of interest rules, and ensuring that campaign donations don't influence government decisions. This will reduce costs for residents and ensure the city gets the best services.",
                "topic": "governance",
                "subtopic": "ethics_reform",
                "keywords": ["pay-to-play", "merit-based contracts", "public dashboards", "transparency", "conflict of interest", "campaign donations"]
            }
        ]
        
        for policy_data in policies:
            source = KnowledgeSource(
                url="https://www.ali2025.com/policies",
                title="Ali 2025 Policy Platform",
                source_type="campaign_policy",
                credibility=SourceCredibility.PRIMARY,
                language="en"
            )
            
            item = KnowledgeItem(
                id=policy_data["id"],
                content=policy_data["content"],
                content_type=ContentType.POLICY,
                topic=policy_data["topic"],
                subtopic=policy_data["subtopic"],
                keywords=policy_data["keywords"],
                sources=[source],
                confidence_score=1.0,
                language="en"
            )
            
            success = self.kb.add_knowledge_item(item)
            if success:
                logger.info(f"Loaded policy: {policy_data['id']}")
            else:
                logger.error(f"Failed to load policy: {policy_data['id']}")
    
    def load_biographical_information(self):
        """Load biographical information about Mussab Ali"""
        
        bio_items = [
            {
                "id": "bio_education_harvard",
                "content": "Mussab Ali attended Harvard Law School after the COVID-19 pandemic, demonstrating his commitment to public service and legal expertise. His legal education provides him with the knowledge and skills necessary to navigate complex municipal law and policy issues as mayor.",
                "topic": "personal_background",
                "subtopic": "education",
                "keywords": ["Harvard Law School", "legal education", "COVID-19", "municipal law", "policy expertise"]
            },
            {
                "id": "bio_health_journey",
                "content": "Mussab Ali is a cancer survivor who overcame significant health challenges while pursuing his education and public service career. This experience has given him resilience, perspective, and a deep understanding of healthcare challenges facing Jersey City residents.",
                "topic": "personal_background", 
                "subtopic": "health_journey",
                "keywords": ["cancer survivor", "health challenges", "resilience", "healthcare", "personal experience"]
            },
            {
                "id": "bio_school_board_service",
                "content": "Mussab Ali served as Jersey City School Board President, making him the youngest person ever elected to that position. During his tenure, he oversaw significant improvements including rising graduation rates, increased teacher pay, removal of lead from school drinking water, and providing free prescription glasses to students. He is the only mayoral candidate to have held city-wide elected office in Jersey City.",
                "topic": "public_service",
                "subtopic": "school_board",
                "keywords": ["school board president", "youngest elected", "graduation rates", "teacher pay", "lead removal", "prescription glasses", "city-wide office"]
            },
            {
                "id": "bio_age_generation",
                "content": "At 28 years old, Mussab Ali is the only mayoral candidate under 40, representing a new generation of leadership for Jersey City. His youth is coupled with significant accomplishments and a fresh perspective on the challenges facing the city's diverse, growing population.",
                "topic": "personal_background",
                "subtopic": "generational_change",
                "keywords": ["28 years old", "under 40", "new generation", "fresh perspective", "diverse population", "young leader"]
            }
        ]
        
        for bio_data in bio_items:
            source = KnowledgeSource(
                url="https://www.ali2025.com/about",
                title="About Mussab Ali",
                source_type="campaign_biography",
                credibility=SourceCredibility.PRIMARY,
                language="en"
            )
            
            item = KnowledgeItem(
                id=bio_data["id"],
                content=bio_data["content"], 
                content_type=ContentType.BIOGRAPHY,
                topic=bio_data["topic"],
                subtopic=bio_data["subtopic"],
                keywords=bio_data["keywords"],
                sources=[source],
                confidence_score=1.0,
                language="en"
            )
            
            success = self.kb.add_knowledge_item(item)
            if success:
                logger.info(f"Loaded bio item: {bio_data['id']}")
            else:
                logger.error(f"Failed to load bio item: {bio_data['id']}")

    def load_multilingual_content(self):
        """Load content in multiple languages for key topics"""
        
        # Spanish translations of key FAQs
        spanish_content = [
            {
                "id": "faq_experience_es",
                "content": "Aunque Mussab es joven (tiene 28 años y es el único candidato menor de 40), también es increíblemente talentoso. Después de la pandemia de COVID-19, fue a la Escuela de Derecho de Harvard, venció el cáncer, fue elegido para la junta escolar (el único candidato a alcalde que ocupó un cargo en toda la ciudad en Jersey City), y luego fue elegido como el presidente de junta escolar más joven en la historia de Jersey City. Es joven, pero pensamos que eso es una ventaja, no un defecto para alguien tan talentoso como él.",
                "topic": "candidate_qualifications",
                "keywords": ["experiencia", "joven", "edad", "Harvard", "junta escolar", "presidente", "talentoso"],
                "language": "es"
            },
            {
                "id": "faq_housing_es", 
                "content": "Mussab se compromete a expandir la zonificación para permitir más construcción residencial y aprobar más de 25,000 unidades para satisfacer la demanda de los residentes de Jersey City. También se asegurará de que todos los nuevos edificios tengan unidades de vivienda asequible, limitará los aumentos de alquiler por parte de los desarrolladores y priorizará a los residentes de Jersey City para viviendas asequibles.",
                "topic": "housing",
                "keywords": ["vivienda", "alquiler", "asequible", "apartamentos", "casas", "zonificación", "25000 unidades"],
                "language": "es"
            }
        ]
        
        for content_data in spanish_content:
            source = KnowledgeSource(
                url="https://www.ali2025.com/es",
                title="Campaña Ali 2025",
                source_type="campaign_website",
                credibility=SourceCredibility.PRIMARY,
                language="es"
            )
            
            item = KnowledgeItem(
                id=content_data["id"],
                content=content_data["content"],
                content_type=ContentType.FAQ,
                topic=content_data["topic"],
                keywords=content_data["keywords"],
                sources=[source],
                confidence_score=1.0,
                language=content_data["language"]
            )
            
            success = self.kb.add_knowledge_item(item)
            if success:
                logger.info(f"Loaded Spanish content: {content_data['id']}")
            else:
                logger.error(f"Failed to load Spanish content: {content_data['id']}")

    def load_all_data(self):
        """Load all campaign data into the knowledge base"""
        logger.info("Starting comprehensive data loading...")
        
        try:
            self.load_comprehensive_faqs()
            logger.info("✓ Loaded comprehensive FAQs")
            
            self.load_news_articles()
            logger.info("✓ Loaded news articles")
            
            self.load_policy_positions()
            logger.info("✓ Loaded policy positions")
            
            self.load_biographical_information()
            logger.info("✓ Loaded biographical information")
            
            self.load_multilingual_content()
            logger.info("✓ Loaded multilingual content")
            
            # Print final statistics
            stats = self.kb.get_statistics()
            logger.info(f"Data loading complete! Total items: {stats.get('total_items', 0)}")
            logger.info(f"Languages: {list(stats.get('by_language', {}).keys())}")
            logger.info(f"Topics: {list(stats.get('top_topics', {}).keys())}")
            
        except Exception as e:
            logger.error(f"Error during data loading: {str(e)}")
            raise

def main():
    """Main function to load all campaign data"""
    # Initialize knowledge base
    kb = KnowledgeBaseManager("ali_2025_knowledge.db")
    
    # Create data loader
    loader = CampaignDataLoader(kb)
    
    # Load all data
    loader.load_all_data()
    
    # Test the loaded data with some sample queries
    test_queries = [
        "What experience does Mussab have?",
        "¿Cuál es la política de vivienda de Mussab?",  # Spanish
        "Why did taxes increase when he was school board president?",
        "What is Mussab's plan for public transportation?",
        "How will he fight corruption?"
    ]
    
    print("\n" + "="*60)
    print("TESTING LOADED KNOWLEDGE BASE")
    print("="*60)
    
    for query in test_queries:
        detected_lang = kb.detect_language(query)
        print(f"\nQuery: {query}")
        print(f"Detected Language: {detected_lang}")
        
        results = kb.search_knowledge(query, language=detected_lang, limit=2)
        
        for i, (item, score) in enumerate(results, 1):
            print(f"\nResult {i} (Score: {score:.3f}):")
            print(f"Topic: {item.topic}")
            print(f"Language: {item.language}")
            print(f"Content: {item.content[:200]}...")
            print(f"Sources: {[s.url for s in item.sources]}")

if __name__ == "__main__":
    main()
