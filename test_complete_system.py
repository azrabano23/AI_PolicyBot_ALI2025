#!/usr/bin/env python3
"""
Complete Test Script for Ali 2025 Campaign Bot
Demonstrates the 2-step process: Knowledge Base Retrieval + O3-PRO Enhancement
Supports multilingual queries and empathetic responses
"""

import os
import sys
import logging
from pathlib import Path

# Add backend/src to path so we can import our modules
backend_src_path = Path(__file__).parent / "backend" / "src"
sys.path.insert(0, str(backend_src_path))

from knowledge_base import KnowledgeBaseManager
from data_loader import CampaignDataLoader
from enhanced_response_generator import EnhancedResponseGenerator, ResponseContext

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompleteCampaignSystem:
    """Complete integrated campaign bot system demonstrating all functionality"""
    
    def __init__(self, db_name="ali_2025_complete_test.db"):
        """Initialize the complete system"""
        logger.info("🚀 Initializing Ali 2025 Complete Campaign System")
        
        # Step 1: Initialize Knowledge Base
        self.kb_manager = KnowledgeBaseManager(db_name)
        logger.info("✓ Knowledge Base Manager initialized")
        
        # Step 2: Initialize Enhanced Response Generator
        self.response_generator = EnhancedResponseGenerator(self.kb_manager)
        logger.info("✓ Enhanced Response Generator initialized")
        
        # Load campaign data
        self._load_campaign_data()
        logger.info("🎯 Complete system ready!")
    
    def _load_campaign_data(self):
        """Load all campaign data into the knowledge base"""
        logger.info("📚 Loading comprehensive campaign data...")
        
        try:
            # Check if we already have data
            stats = self.kb_manager.get_statistics()
            if stats.get('total_items', 0) > 0:
                logger.info(f"📊 Knowledge base already contains {stats['total_items']} items")
                return
            
            # Load fresh data
            loader = CampaignDataLoader(self.kb_manager)
            loader.load_all_data()
            
            # Show final stats
            final_stats = self.kb_manager.get_statistics()
            logger.info(f"📊 Loaded {final_stats['total_items']} knowledge items")
            logger.info(f"🌍 Languages: {list(final_stats['by_language'].keys())}")
            logger.info(f"📋 Topics: {list(final_stats['top_topics'].keys())}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load campaign data: {e}")
            raise
    
    def process_query(self, query: str, language: str = None) -> dict:
        """Process a user query through the complete 2-step system"""
        logger.info(f"🔍 Processing query: '{query}'")
        
        # Step 1: Detect language if not provided
        if not language:
            language = self.kb_manager.detect_language(query)
        logger.info(f"🗣️ Language: {language}")
        
        # Step 2: Knowledge Retrieval
        retrieved_facts = self.kb_manager.search_knowledge(query, language=language, limit=10)
        logger.info(f"📖 Retrieved {len(retrieved_facts)} relevant facts")
        
        # Step 3: Response Enhancement with O3-PRO
        context = ResponseContext(
            user_query=query,
            detected_language=language,
            retrieved_facts=retrieved_facts
        )
        
        enhanced_response = self.response_generator.generate_response(context)
        logger.info(f"✨ Generated response with confidence: {enhanced_response['confidence_score']:.2f}")
        
        return enhanced_response
    
    def run_comprehensive_test(self):
        """Run comprehensive tests covering all major functionality"""
        print("\n" + "="*80)
        print("🎭 ALI 2025 COMPREHENSIVE CAMPAIGN BOT TEST")
        print("="*80)
        
        test_scenarios = [
            {
                "name": "Tax Question (Your Example)",
                "query": "When Mussab was school board president the budget went up and my taxes did too — I don't like that.",
                "language": "en",
                "description": "Tests the exact scenario you provided with detailed tax explanation"
            },
            {
                "name": "Experience Challenge",
                "query": "Mussab doesn't have any experience – why should I vote for him?",
                "language": "en",
                "description": "Addresses experience concerns with Harvard, cancer survival, school board achievements"
            },
            {
                "name": "Spanish Housing Question",
                "query": "¿Cuál es el plan de vivienda de Mussab? No puedo pagar el alquiler.",
                "language": "es",
                "description": "Tests Spanish language support for housing policy"
            },
            {
                "name": "Transportation Query",
                "query": "Public transit is terrible and expensive. What's Mussab going to do?",
                "language": "en",
                "description": "Tests transportation policy with free buses and congestion pricing"
            },
            {
                "name": "Corruption Concerns",
                "query": "I'm sick of corruption in Jersey City! How will Mussab be different?",
                "language": "en",
                "description": "Tests anti-corruption messaging and pay-to-play reform"
            },
            {
                "name": "Faith Question",
                "query": "Why does Mussab talk so much about his faith?",
                "language": "en",
                "description": "Tests sensitive faith-based messaging and 9/11 reference"
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{'🔥'*60}")
            print(f"TEST {i}: {scenario['name']}")
            print(f"{'🔥'*60}")
            print(f"QUERY: {scenario['query']}")
            print(f"LANGUAGE: {scenario['language']}")
            print(f"PURPOSE: {scenario['description']}")
            print("\n📝 RESPONSE:")
            print("-" * 60)
            
            try:
                result = self.process_query(scenario['query'], scenario['language'])
                
                # Print the response
                print(result['response'])
                
                # Print metadata
                print("\n📊 RESPONSE ANALYSIS:")
                print(f"  • Confidence Score: {result['confidence_score']:.2f}")
                print(f"  • Response Type: {result['response_type']}")
                print(f"  • Language: {result['language']}")
                print(f"  • Topics Covered: {', '.join(result['topics_covered'])}")
                print(f"  • Sources Used: {len(result['sources'])} sources")
                
                if result['sources']:
                    print(f"  • Source Examples:")
                    for source in result['sources'][:2]:
                        print(f"    - {source['title']} ({source['credibility']})")
                
            except Exception as e:
                print(f"❌ ERROR: {e}")
                logger.error(f"Test failed: {e}", exc_info=True)
        
        print(f"\n{'🎉'*60}")
        print("COMPREHENSIVE TEST COMPLETE!")
        print(f"{'🎉'*60}")
    
    def interactive_mode(self):
        """Run in interactive mode for live testing"""
        print("\n" + "="*60)
        print("🤖 ALI 2025 INTERACTIVE CAMPAIGN ASSISTANT")
        print("="*60)
        print("Enter questions about Mussab Ali's campaign.")
        print("Supports English, Spanish, Arabic, and French.")
        print("Type 'quit' to exit, 'stats' for knowledge base statistics.")
        print("="*60)
        
        while True:
            try:
                query = input("\n💬 Your Question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for testing the Ali 2025 Campaign Bot!")
                    break
                
                if query.lower() == 'stats':
                    stats = self.kb_manager.get_statistics()
                    print(f"\n📊 KNOWLEDGE BASE STATISTICS:")
                    print(f"  • Total Items: {stats['total_items']}")
                    print(f"  • Languages: {list(stats['by_language'].keys())}")
                    print(f"  • Top Topics: {list(stats['top_topics'].keys())}")
                    continue
                
                if not query:
                    print("Please enter a question about the campaign.")
                    continue
                
                print("\n🤔 Processing your question...")
                result = self.process_query(query)
                
                print(f"\n🎯 RESPONSE:")
                print("-" * 50)
                print(result['response'])
                print(f"\n(Confidence: {result['confidence_score']:.2f}, "
                      f"Language: {result['language']}, "
                      f"Sources: {len(result['sources'])})")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for testing!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                logger.error(f"Interactive mode error: {e}")

def main():
    """Main function to run the complete system test"""
    try:
        # Initialize the complete system
        system = CompleteCampaignSystem()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == "--interactive":
                system.interactive_mode()
                return
            elif sys.argv[1] == "--test":
                system.run_comprehensive_test()
                return
        
        # Default: run comprehensive test
        system.run_comprehensive_test()
        
        # Offer interactive mode
        print("\n" + "="*60)
        response = input("🎮 Would you like to try interactive mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            system.interactive_mode()
        
    except Exception as e:
        logger.error(f"System initialization failed: {e}", exc_info=True)
        print(f"\n❌ System Error: {e}")
        print("Please check your OpenAI API key and dependencies.")

if __name__ == "__main__":
    main()
