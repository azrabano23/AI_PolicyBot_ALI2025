from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import openai
import os
from datetime import datetime, timedelta
import json
import time
from urllib.parse import urljoin, urlparse
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
ALI_WEBSITE_BASE_URL = "https://www.ali2025.com/"
CACHE_DURATION = 300  # 5 minutes in seconds

# In-memory cache for website content
website_cache = {
    'content': {},
    'last_updated': None
}

class Ali2025WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_page_content(self, url):
        """Fetch and parse content from a webpage"""
        try:
            logger.info(f"Fetching content from: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return {
                'url': url,
                'title': soup.title.string if soup.title else 'No title',
                'content': text[:8000],  # Increased content length for more context
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def discover_pages(self):
        """Discover important pages from the website"""
        pages_to_scrape = [self.base_url]
        
        try:
            # Get main page and find important links
            main_page = self.get_page_content(self.base_url)
            if main_page:
                soup = BeautifulSoup(requests.get(self.base_url).content, 'html.parser')
                
                # Look for navigation links and important pages
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(self.base_url, href)
                    
                    # Only include pages from the same domain
                    if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                        # Look for policy-related pages
                        if any(keyword in href.lower() for keyword in 
                               ['policy', 'issues', 'platform', 'about', 'biography', 'vision', 'plan']):
                            pages_to_scrape.append(full_url)
                
                # Remove duplicates
                pages_to_scrape = list(set(pages_to_scrape))
                
        except Exception as e:
            logger.error(f"Error discovering pages: {str(e)}")
        
        return pages_to_scrape[:10]  # Limit to 10 pages
    
    def scrape_website(self):
        """Scrape the entire website and return structured content"""
        pages = self.discover_pages()
        scraped_content = {}
        
        for page_url in pages:
            content = self.get_page_content(page_url)
            if content:
                scraped_content[page_url] = content
            time.sleep(1)  # Be respectful to the server
        
        return scraped_content

class Ali2025ChatBot:
    def __init__(self):
        # Initialize OpenAI client - you'll need to set your API key
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        self.system_prompt = """You are the official Ali 2025 Campaign Assistant for Mussab Ali's 2025 Jersey City mayoral campaign. 
        You are an expert on all aspects of the campaign and should provide DETAILED, COMPREHENSIVE, and THOROUGH responses.
        
        RESPONSE GUIDELINES:
        - Always provide detailed, in-depth answers (aim for 3-5 paragraphs minimum)
        - Include specific policy details, background context, and implementation plans when available
        - Explain the 'why' behind policies and how they benefit Jersey City residents
        - Use concrete examples and specific benefits whenever possible
        - Connect policies to real Jersey City challenges and opportunities
        - Be enthusiastic and inspiring about the campaign's vision
        
        You have access to real-time information from ali2025.com and should provide comprehensive information about:

        1. Mussab Ali's detailed policies and platform - explain each policy thoroughly
        2. Campaign events and updates - provide context and significance
        3. How people can get involved or volunteer - give specific steps and opportunities
        4. Comprehensive background information about Mussab Ali and his team
        5. Jersey City issues and Ali's detailed proposed solutions
        6. The vision for Jersey City's future under Ali's leadership

        Always be professional, enthusiastic about the campaign, and encourage civic engagement. 
        Provide educational content about local government and civic participation.
        When you don't have specific information, direct users to visit ali2025.com for the most current details.
        Always cite your sources and encourage users to get involved in the campaign."""
    
    def generate_response(self, user_message, website_content):
        """Generate a response using OpenAI with website context"""
        try:
            # Prepare context from website content
            context = ""
            sources = []
            
            for url, content in website_content.items():
                context += f"\n\nFrom {content['title']} ({url}):\n{content['content'][:1200]}"  # Balanced content for context
                sources.append({
                    'url': url,
                    'title': content['title']
                })
            
            # Create the full prompt
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": f"Current website content:\n{context}"},
                {"role": "user", "content": user_message}
            ]
            
            # Use OpenAI API (you can replace this with any other AI service)
            if openai.api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=800,  # Longer responses but stable
                    temperature=0.7,
                    request_timeout=10
                )
                
                return {
                    'response': response.choices[0].message.content,
                    'sources': sources[:3]  # Limit to 3 sources
                }
            else:
                # Fallback response when no API key is available
                return {
                    'response': f"I'd be happy to help you learn about Mussab Ali's 2025 campaign! Based on the latest information from ali2025.com, I can assist with questions about policies, events, and how to get involved. However, I need an OpenAI API key to provide detailed responses. For now, please visit ali2025.com directly for the most current campaign information.",
                    'sources': sources[:3]
                }
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                'response': "I'm experiencing some difficulty right now. Please visit ali2025.com for the latest campaign information, or try asking your question again.",
                'sources': []
            }

# Initialize components
scraper = Ali2025WebScraper(ALI_WEBSITE_BASE_URL)
chatbot = Ali2025ChatBot()

def update_website_cache():
    """Update the website content cache"""
    global website_cache
    
    current_time = datetime.now()
    
    # Check if cache needs updating
    if (website_cache['last_updated'] is None or 
        current_time - website_cache['last_updated'] > timedelta(seconds=CACHE_DURATION)):
        
        logger.info("Updating website cache...")
        try:
            fresh_content = scraper.scrape_website()
            website_cache['content'] = fresh_content
            website_cache['last_updated'] = current_time
            logger.info(f"Cache updated with {len(fresh_content)} pages")
        except Exception as e:
            logger.error(f"Error updating cache: {str(e)}")

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
        
        # Update cache if needed
        update_website_cache()
        
        # Generate response
        response_data = chatbot.generate_response(user_message, website_cache['content'])
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': "I'm experiencing technical difficulties. Please visit ali2025.com for campaign information.",
            'sources': []
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'cache_last_updated': website_cache['last_updated'].isoformat() if website_cache['last_updated'] else None,
        'cached_pages': len(website_cache['content'])
    })

@app.route('/api/refresh-cache', methods=['POST'])
def refresh_cache():
    """Manually refresh the website cache"""
    global website_cache
    website_cache['last_updated'] = None  # Force cache update
    update_website_cache()
    
    return jsonify({
        'message': 'Cache refreshed successfully',
        'cached_pages': len(website_cache['content'])
    })

if __name__ == '__main__':
    # Initial cache load
    update_website_cache()
    
    # Run the Flask app
    port = int(os.getenv('PORT', 8081))
    app.run(debug=True, host='0.0.0.0', port=port)
