# Ali 2025 Campaign Bot 🇺🇸

**The Official AI-Powered Campaign Assistant for Mussab Ali's 2025 Jersey City Mayoral Campaign**

🔥 **This intelligent chatbot now works like ChatGPT for your campaign!** It provides comprehensive, detailed responses to voter questions about Mussab Ali's policies, experience, and vision for Jersey City. Built specifically for campaign volunteers, staff, and voters to get in-depth information instantly.

## 🚀 **NEW: Enhanced ChatGPT-Like Experience**

- 🧠 **OpenAI GPT-3.5 Integration**: Provides comprehensive, multi-paragraph responses
- 📚 **Detailed Policy Explanations**: 4-6 paragraph responses with implementation details
- 🎯 **Smart FAQ System**: 18+ pre-programmed responses for common voter questions
- 🔄 **Hybrid Intelligence**: Combines pre-programmed accuracy with AI flexibility
- 📖 **Educational Content**: Explains the 'why' behind policies with context and examples

## ✨ Key Features

- 🤖 **ChatGPT-Level Responses**: Comprehensive, detailed answers that rival professional AI assistants
- 🎠 **Interactive Question Carousel**: Beautiful rotating display of 18 key campaign topics
- 🇺🇸 **Patriotic Design**: Red, white, and blue theme reflecting American values
- 📱 **Mobile-Friendly**: Works perfectly on phones, tablets, and computers
- ⚡ **Real-Time Updates**: Automatically pulls latest info from ali2025.com
- 🎯 **Campaign-Focused**: Addresses real voter concerns with Mussab's actual positions
- 📊 **Source Attribution**: Every answer includes links to official campaign materials
- 🔄 **Auto-Advancing Carousel**: Questions rotate every 5 seconds with manual controls

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

## 🚀 Quick Start Guide for Campaign Interns

**This is the easiest way to get the bot running on your computer in under 5 minutes!**

### Step 1: Get the Code 📥
```bash
# Clone the repository to your computer
git clone https://github.com/azrabano23/AI_PolicyBot_ALI2025.git
cd AI_PolicyBot_ALI2025
```

### Step 2: Set Up the Backend (Server) 🔧
```bash
# Go to backend folder
cd backend

# Create a virtual environment (keeps everything organized)
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Set Up the Frontend (Website) 🎨
```bash
# Go to frontend folder (open a new terminal window)
cd frontend

# Install required packages
npm install
```

### Step 4: You're Ready! ✅
That's it! No API keys needed - the bot works perfectly with Mussab's pre-programmed responses.

---

## 📋 Detailed Setup (if you need more help)

### 1. Clone and Navigate
```bash
cd AI_PolicyBot_ALI2025
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
cp .env.example .env
# Edit .env and add your OpenAI API key if you have one
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install
```

## 🏃‍♂️ Running the Application (Campaign Interns)

**Follow these exact steps every time you want to use the bot:**

### 🔴 Step 1: Start the Backend (Server)
**Open Terminal/Command Prompt #1:**
```bash
cd AI_PolicyBot_ALI2025/backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python src/app.py
```
✅ **Success!** You should see:
- "Updating website cache..."
- "Running on http://127.0.0.1:8084"
- "Debugger is active!"

👉 **Keep this terminal window open!**

### 🔵 Step 2: Start the Frontend (Website)
**Open Terminal/Command Prompt #2:**
```bash
cd AI_PolicyBot_ALI2025/frontend
npm start
```
✅ **Success!** You should see:
- "Compiled successfully!"
- "Local: http://localhost:3000" (or similar)
- Your browser should automatically open

### 🎉 Step 3: Start Using the Bot!
1. Your browser should open automatically to the bot
2. If not, go to: **http://localhost:3000** (or the URL shown in terminal)
3. You'll see a beautiful patriotic interface with a question carousel
4. Click on any question in the carousel or type your own!

---

## 🔧 Advanced Running (Technical Details)

### Backend Details
- **Port**: 8084
- **URL**: http://localhost:8084
- **Health Check**: http://localhost:8084/api/health

### Frontend Details  
- **Port**: Usually 3000, 3001, or 3002 (automatically assigned)
- **Development Server**: React development server with hot reload

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

## 🆘 Troubleshooting for Campaign Interns

### Common Issues and Solutions

#### Problem: "Port already in use" error
**Solution:** 
```bash
# Kill any existing Python processes
pkill -f python
# Then restart the backend
```

#### Problem: Frontend won't start or shows errors
**Solution:**
```bash
# Clear npm cache and reinstall
cd frontend
npm cache clean --force
rm -rf node_modules
npm install
npm start
```

#### Problem: "Command not found: python3"
**Solution:**
- On Mac: Install Python from python.org or use `python` instead of `python3`
- On Windows: Install Python from Microsoft Store or python.org

#### Problem: "Command not found: npm"
**Solution:**
- Install Node.js from nodejs.org (includes npm)

#### Problem: Bot gives generic responses instead of specific FAQ answers
**Solution:**
- Make sure you're using keywords from the carousel questions
- Try exact phrases like "experience", "schools", "housing", "corruption"

### 📞 Getting Help
1. Check this README first
2. Ask a tech-savvy campaign volunteer
3. Create an issue on GitHub
4. Contact the tech team

### 🎯 Quick Test
To make sure everything works:
1. Visit http://localhost:3000 (or your frontend URL)
2. Click on any question in the carousel
3. You should get a specific, detailed response about Mussab's position
4. Try typing "experience" - you should get info about Mussab's qualifications

---

## 📊 What Questions Does the Bot Answer?

The bot has specific, detailed responses for these 18 key voter concerns:

### About Mussab
1. **Experience**: "Mussab doesn't have any experience – why should I vote for him?"
2. **Policies**: "Mussab just has talking points but no concrete policy proposals."
3. **Taxes**: "When he was president the school board budget increased which led to higher taxes"
4. **Corruption**: "There is a lot of corruption on the school board..."
5. **Credibility**: "I haven't heard of him before – is Mussab a serious candidate?"
6. **Faith**: "Why is Mussab's faith so important to him?"

### Policy Issues
7. **Safety**: "Jersey City has gotten more dangerous over the years"
8. **Transit**: "Public transit is more expensive and worse quality than ever"
9. **Housing**: "I can't afford to buy a house in Jersey City anymore"
10. **Jobs**: "It's hard to find a good job with a fair wage"
11. **Schools**: "The public schools for my kids aren't very good"
12. **Climate**: "What is Mussab going to do to combat climate change?"
13. **Corruption (General)**: "I'm sick of all the corruption in our city!"

### Against Other Candidates
14. **Pro-Fulop voters**: "I really liked our previous Mayor Fulop"
15. **Anti-Fulop voters**: "I disliked our previous Mayor Fulop"
16. **McGreevey supporters**: "I want to vote for Jim McGreevey"
17. **O'Dea supporters**: "I want to vote for Bill O'Dea"
18. **Solomon supporters**: "I want to vote for James Solomon"

---

## 🔧 Technical Documentation

### How the System Works

This bot uses a **hybrid intelligence approach** combining pre-programmed FAQ responses with OpenAI's GPT-3.5 for comprehensive answers:

1. **User Query Processing**: When a user asks a question, the system first checks if it matches any of the 18 pre-programmed FAQ topics
2. **Keyword Matching**: Uses sophisticated keyword matching to identify relevant FAQ topics
3. **FAQ Priority**: If a match is found, returns the exact campaign-approved response
4. **AI Fallback**: For questions not covered by FAQs, the system uses OpenAI GPT-3.5 with campaign context
5. **Website Context**: All AI responses include real-time context from ali2025.com

### File Structure Explained

#### Backend Files (`/backend/`)

**`src/app.py`** - The main Flask application file containing:
- `Ali2025WebScraper` class: Handles website scraping and content discovery
- `Ali2025ChatBot` class: Manages FAQ responses and OpenAI integration
- API endpoints: `/api/chat`, `/api/health`, `/api/refresh-cache`
- Caching system: 5-minute cache for website content
- Environment configuration and error handling

**`requirements.txt`** - Python dependencies:
```
Flask==2.3.2
Flask-CORS==4.0.0
requests==2.31.0
beautifulsoup4==4.12.2
openai==0.27.8
python-dotenv==1.0.0
gunicorn==21.2.0
```

**`.env`** - Environment variables (created during setup):
- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Backend server port (default: 8085)
- `ALI_WEBSITE_URL`: Campaign website URL
- `CACHE_DURATION`: How long to cache website content

#### Frontend Files (`/frontend/`)

**`src/components/Ali2025AdvancedBot.jsx`** - Main React component containing:
- Chat interface with message history
- Interactive question carousel with 18 pre-defined questions
- Auto-advancing carousel (5-second intervals)
- Real-time API communication with backend
- Responsive design with Tailwind CSS
- Source attribution and link handling

**`package.json`** - Frontend dependencies including:
- React 18+ for UI framework
- Tailwind CSS for styling
- Lucide React for icons
- Development and build scripts

**`tailwind.config.js`** - Tailwind CSS configuration:
- Custom color schemes for patriotic theme
- Responsive breakpoints
- Animation configurations

### API Communication Flow

1. **User Input**: User types question or clicks carousel item
2. **Frontend Processing**: React component sends POST request to `/api/chat`
3. **Backend Processing**:
   - Checks FAQ keywords first
   - If no match, scrapes latest website content
   - Sends to OpenAI with campaign context
   - Returns formatted response with sources
4. **Frontend Display**: Shows response with typing animation and source links

### FAQ Keyword System

Each of the 18 FAQ topics has specific keywords that trigger responses:

```javascript
"experience": {
    "keywords": ["experience", "inexperienced", "young", "qualify", "qualified", "age", "too young"]
},
"housing": {
    "keywords": ["housing", "rent", "afford", "expensive", "house", "apartment", "affordable"]
}
```

### OpenAI Integration Details

**Model**: GPT-3.5-turbo
**Max Tokens**: 1200 (for comprehensive responses)
**Temperature**: 0.7 (balanced creativity)
**System Prompt**: Detailed instructions for campaign-focused responses

### Caching Strategy

- **Website Content**: Cached for 5 minutes to balance freshness with performance
- **Automatic Refresh**: Cache updates automatically when expired
- **Manual Refresh**: Available via `/api/refresh-cache` endpoint
- **Error Handling**: Graceful fallback when scraping fails

### Security Considerations

- **API Key Protection**: OpenAI key stored in environment variables
- **CORS Configuration**: Proper cross-origin request handling
- **Input Validation**: User input sanitization and validation
- **Rate Limiting**: Built-in protection against spam

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 🏆 Built for the Ali 2025 Campaign

**Mussab Ali for Jersey City Mayor 2025**
- 🌐 Website: [ali2025.com](https://www.ali2025.com/)
- 📧 Contact: [info@ali2025.com](mailto:info@ali2025.com)
- 📱 Follow us on social media for updates

*This tool was created to help campaign volunteers and staff provide accurate, consistent information to voters about Mussab Ali's vision for Jersey City.*
