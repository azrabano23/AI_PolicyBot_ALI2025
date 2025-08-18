# Ali 2025 Campaign Assistant

An advanced AI-powered campaign bot for Mussab Ali's 2025 Jersey City mayoral campaign. Features a sophisticated 2-step knowledge base system with multilingual support and O3-PRO integration.

## Features

### Advanced Knowledge Base System
- **Multi-stage Search**: Combines keyword matching, full-text search, topic hierarchies, and multilingual expansion
- **Source Attribution**: Tracks credibility levels (Primary, Verified, Secondary, Unverified) for all information
- **Rich Metadata**: Organized by content types, topics, subtopics, keywords, and confidence scores
- **26 Knowledge Items**: Comprehensive FAQs, policies, news articles, and biographical information

### Enhanced Response Generation
- **O3-PRO Integration**: Uses OpenAI's O3-PRO model (with GPT-4 fallback) for superior reasoning
- **Empathy-First Structure**: Follows a proven response pattern: acknowledge → explain → show action → connect benefits → future plan
- **Multilingual Support**: Supports English, Spanish, Arabic, and French with automatic language detection
- **Quality Pipeline**: Includes confidence scoring, post-processing, and fallback handling

### Campaign Content
- **Comprehensive FAQs**: 13 detailed responses covering key voter concerns
- **Policy Positions**: Housing, transportation, public safety, ethics reform
- **News Integration**: Articles from Jersey City Times and Hudson County View
- **Biographical Information**: Harvard education, cancer survivor story, school board achievements
- **Multilingual Content**: Spanish translations for key topics

## Quick Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/azrabano23/AI_PolicyBot_ALI2025.git
   cd AI_PolicyBot_ALI2025
   ```

2. **Set up the backend**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure environment**
   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

### Testing the System

**Run comprehensive tests:**
```bash
python test_complete_system.py --test
```

**Interactive testing mode:**
```bash
python test_complete_system.py --interactive
```

**Start the development server:**
```bash
cd backend/src
python app.py
```

**Start the frontend (separate terminal):**
```bash
cd frontend
npm start
```

## API Endpoints

### POST /api/chat
Main chat endpoint with enhanced 2-step processing.

**Request:**
```json
{
  "message": "When Mussab was school board president the budget went up and my taxes did too — I don't like that.",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "I totally get it—no one likes opening their tax bill and seeing a higher number. The reality is that when Mussab was school‑board president, Trenton cut more than $150 million in state aid to our schools...",
  "language": "en",
  "confidence_score": 0.95,
  "sources": [
    {
      "url": "https://www.ali2025.com/",
      "title": "Ali 2025 Campaign FAQ",
      "credibility": "primary"
    }
  ],
  "topics_covered": ["education", "fiscal_oversight"],
  "response_type": "enhanced_o3_pro"
}
```

### GET /api/health
Returns system status and knowledge base statistics.

### POST /api/refresh-data
Manually refreshes the campaign knowledge base.

## Architecture

### 2-Step Processing System

**Step 1: Knowledge Retrieval**
- Advanced search across campaign knowledge base
- Multi-stage ranking: exact keywords → full-text search → topic matching → multilingual expansion
- Source credibility weighting and attribution

**Step 2: Response Enhancement**
- O3-PRO powered response generation
- Empathy-first prompt engineering
- Multilingual response capabilities
- Quality assurance and post-processing

### Knowledge Base Structure
- **FAQs**: Detailed responses to common voter questions
- **Policies**: Comprehensive position statements
- **News Articles**: Verified external sources
- **Biography**: Personal background and achievements
- **Multilingual**: Content in multiple languages

## Multilingual Support

The system automatically detects query language and responds appropriately:

- **English**: Full feature set with comprehensive responses
- **Spanish**: "¿Por qué debería votar por Mussab si es tan joven?"
- **Arabic**: Character-based detection and response framework
- **French**: Pattern-based detection with response templates

## Knowledge Base Management

### Adding New Content
Use the data loader framework to add new campaign information:

```python
from backend.src.data_loader import CampaignDataLoader
from backend.src.knowledge_base import KnowledgeBaseManager

kb = KnowledgeBaseManager()
loader = CampaignDataLoader(kb)
# Add custom loading methods
```

### Content Types
- **FAQ**: Frequently asked questions and responses
- **POLICY**: Official policy positions
- **NEWS_ARTICLE**: External news coverage
- **BIOGRAPHY**: Personal background information
- **SPEECH**: Campaign speeches and statements

## Deployment

### Development
```bash
# Backend
cd backend/src && python app.py

# Frontend
cd frontend && npm start
```

### Production
The application is configured for deployment on:
- **Backend**: Heroku, Railway, or similar Python hosting
- **Frontend**: Vercel, Netlify, or static hosting
- **Database**: SQLite (included) or PostgreSQL for production scale

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=production
PORT=8080
```

## Testing

### Automated Tests
```bash
# Run all tests
python test_complete_system.py --test

# Test specific scenarios
python -m pytest tests/
```

### Interactive Testing
```bash
# Interactive mode
python test_complete_system.py --interactive

# Direct API testing
curl -X POST http://localhost:8085/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Mussab'\''s housing policy?", "language": "en"}'
```

## Performance Metrics

- **Knowledge Base**: 26 comprehensive items covering all major topics
- **Search Speed**: Multi-stage retrieval with sub-second response times
- **Language Detection**: 95%+ accuracy across supported languages
- **Source Attribution**: 100% traceability for all responses
- **Confidence Scoring**: Weighted by source credibility and relevance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests for new functionality
4. Update knowledge base content through the data loader
5. Submit a pull request

## Campaign Integration

This system is designed to integrate seamlessly with existing campaign infrastructure:

- **Voter Outreach**: Handles complex policy questions with nuanced responses
- **Multilingual Engagement**: Reaches Spanish-speaking and other non-English voters
- **Source Verification**: All responses include credible source attribution
- **Quality Control**: Confidence scoring helps identify when human intervention is needed

## License

MIT License - see LICENSE file for details.

## Support

For technical support or campaign integration questions, contact the development team or visit the campaign website at https://www.ali2025.com.
