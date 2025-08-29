from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

from knowledge_base import KnowledgeBaseManager
from enhanced_response_generator import EnhancedResponseGenerator, ResponseContext
from data_loader import CampaignDataLoader

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the application
app = Flask(__name__)
CORS(app)

# --- Global Components ---
# Initialize Knowledge Base
try:
    kb_manager = KnowledgeBaseManager("ali_2025_knowledge.db")
    logger.info("Successfully initialized Knowledge Base Manager.")
except Exception as e:
    logger.error(f"Failed to initialize Knowledge Base Manager: {e}", exc_info=True)
    kb_manager = None

# Initialize Enhanced Response Generator
try:
    response_generator = EnhancedResponseGenerator(kb_manager)
    logger.info("Successfully initialized Enhanced Response Generator.")
except Exception as e:
    logger.error(f"Failed to initialize Enhanced Response Generator: {e}", exc_info=True)
    response_generator = None

def load_initial_data():
    """Load initial campaign data into the knowledge base"""
    try:
        if kb_manager:
            stats = kb_manager.get_statistics()
            if stats.get('total_items', 0) == 0:
                logger.info("Knowledge base is empty. Loading initial data...")
                loader = CampaignDataLoader(kb_manager)
                loader.load_all_data()
                logger.info("Initial data loading complete.")
            else:
                logger.info(f"Knowledge base already contains {stats['total_items']} items. Skipping initial data load.")
    except Exception as e:
        logger.error(f"Failed to load initial data: {e}", exc_info=True)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint with integrated knowledge base and O3-PRO"""
    try:
        if not kb_manager or not response_generator:
            return jsonify({
                'response': "I'm currently experiencing some technical difficulties. Please try again later.",
                'sources': []
            }), 503  # Service Unavailable

        data = request.get_json()
        user_message = data.get('message', '')
        language = data.get('language', 'en')

        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
        
        logger.info(f"Received message: '{user_message}' in language: '{language}'")

        # Step 1: Retrieval - Search knowledge base
        detected_lang = kb_manager.detect_language(user_message)
        logger.info(f"Detected language from message: '{detected_lang}'")
        
        # Use provided language, but fallback to detected
        final_language = language if language in ['en', 'es', 'ar', 'fr'] else detected_lang
        
        retrieved_facts = kb_manager.search_knowledge(user_message, language=final_language, limit=10)
        logger.info(f"Retrieved {len(retrieved_facts)} facts from the knowledge base.")

        # Step 2: Enhancement - Generate response with O3-PRO
        response_context = ResponseContext(
            user_query=user_message,
            detected_language=final_language,
            retrieved_facts=retrieved_facts
        )
        
        enhanced_response = response_generator.generate_response(response_context)
        
        logger.info(f"Generated response with confidence: {enhanced_response['confidence_score']:.2f}")
        
        return jsonify(enhanced_response)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        return jsonify({
            'response': "I'm experiencing technical difficulties. Please visit ali2025.com for campaign information.",
            'sources': []
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint with knowledge base status"""
    kb_stats = {}
    if kb_manager:
        kb_stats = kb_manager.get_statistics()
        
    return jsonify({
        'status': 'healthy',
        'knowledge_base_status': {
            'initialized': kb_manager is not None,
            'total_items': kb_stats.get('total_items', 0),
            'languages': list(kb_stats.get('by_language', {}).keys())
        },
        'response_generator_status': {
            'initialized': response_generator is not None
        }
    })

@app.route('/api/refresh-data', methods=['POST'])
def refresh_data():
    """Manually refresh the campaign knowledge base data"""
    try:
        logger.info("Manual data refresh triggered.")
        load_initial_data()
        return jsonify({'message': 'Campaign data refreshed successfully.'})
    except Exception as e:
        logger.error(f"Failed to refresh data: {e}", exc_info=True)
        return jsonify({'error': 'Failed to refresh data'}), 500

if __name__ == '__main__':
    # Load initial campaign data on startup
    load_initial_data()
    
    # Run the Flask app
    port = int(os.getenv('PORT', 3000))
    is_production = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('PORT')
    debug_mode = not is_production and os.getenv('FLASK_ENV') == 'development'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
