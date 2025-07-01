# Ali 2025 Campaign Bot

An AI-powered campaign assistant for Mussab Ali's 2025 Jersey City mayoral campaign. This bot provides real-time information about policies, campaign events, and volunteer opportunities by scraping the official ali2025.com website.

## Features

- 🤖 AI-powered chat interface
- 🔄 Real-time website scraping from ali2025.com
- 📱 Responsive React frontend
- 🌐 Flask backend with RESTful API
- 📚 Policy and campaign information
- 🎯 Quick question templates
- 📖 Source attribution for responses

## Project Structure

```
ali2025-bot/
├── frontend/          # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   └── Ali2025AdvancedBot.jsx
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
├── backend/           # Flask backend API
│   ├── src/
│   │   └── app.py
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Prerequisites

- Node.js (v16 or higher)
- Python 3.8+
- OpenAI API key (optional, for AI responses)

## Quick Setup

### 1. Clone and Navigate
```bash
cd ali2025-bot
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key if you have one
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python src/app.py
```
Backend will run on http://localhost:5000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```
Frontend will run on http://localhost:3000

## Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
ALI_WEBSITE_URL=https://www.ali2025.com/
CACHE_DURATION=300
```

**Note:** The bot will work without an OpenAI API key, but responses will be limited to cached website content.

## API Endpoints

- `POST /api/chat` - Send a message to the bot
- `GET /api/health` - Check backend health and cache status
- `POST /api/refresh-cache` - Manually refresh website content cache

## Features Explained

### Web Scraping
- Automatically discovers and scrapes relevant pages from ali2025.com
- Caches content for 5 minutes to reduce server load
- Focuses on policy, biography, and campaign-related pages

### AI Chat
- Uses OpenAI GPT-3.5-turbo for intelligent responses
- Provides context from scraped website content
- Includes source attribution for transparency

### Frontend
- Clean, responsive design with Tailwind CSS
- Quick question templates for common inquiries
- Real-time chat interface with typing indicators
- Source links for referenced information

## Customization

### Adding New Quick Questions
Edit `frontend/src/components/Ali2025AdvancedBot.jsx` and modify the `quickQuestions` array:

```javascript
const quickQuestions = [
  { icon: Home, text: "Your custom question", category: "policy" },
  // Add more questions...
];
```

### Modifying Scraping Behavior
Edit `backend/src/app.py` in the `Ali2025WebScraper` class to:
- Change which pages are discovered and scraped
- Modify content extraction logic
- Adjust caching duration

### Styling Changes
- Edit Tailwind classes in the React component
- Modify `frontend/tailwind.config.js` for theme customization
- Update CSS in `frontend/src/App.css` or `frontend/src/index.css`

## Deployment

### Backend Deployment
The backend can be deployed to platforms like:
- Heroku
- DigitalOcean App Platform
- AWS EC2
- Google Cloud Run

Use `gunicorn` for production:
```bash
gunicorn --bind 0.0.0.0:5000 src.app:app
```

### Frontend Deployment
Build the frontend and deploy to:
- Netlify
- Vercel
- AWS S3 + CloudFront

```bash
npm run build
# Deploy the 'build' folder
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for the Ali 2025 campaign. Please respect the campaign's intellectual property and use responsibly.

## Support

For technical issues or questions about the campaign, visit [ali2025.com](https://www.ali2025.com/) or contact the campaign directly.

---

**Built with ❤️ for the Ali 2025 Campaign**
