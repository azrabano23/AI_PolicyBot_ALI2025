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
        
        # Reputable sources for external information
        self.reputable_sources = {
            'jersey_city_gov': 'https://www.jerseycitynj.gov/',
            'nj_gov': 'https://www.nj.gov/',
            'hudson_county': 'https://www.hudsoncountynj.org/',
            'jersey_journal': 'https://www.nj.com/hudson/',
            'tap_into_jc': 'https://www.tapinto.net/towns/jersey-city',
            'njcom_politics': 'https://www.nj.com/politics/',
            'jersey_city_times': 'https://jerseycitytimes.com/',
            'vote411': 'https://www.vote411.org/ballot',
            'ballotpedia': 'https://ballotpedia.org/Jersey_City,_New_Jersey'
        }
    
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
    
    def search_external_sources(self, query, max_sources=3):
        """Search reputable external sources for additional context"""
        external_content = {}
        search_terms = query.lower()
        
        # Define search strategies for different topics
        topic_sources = {
            'jersey city': ['jersey_city_gov', 'jersey_journal', 'tap_into_jc'],
            'education': ['jersey_city_gov', 'nj_gov'],
            'housing': ['jersey_city_gov', 'hudson_county'],
            'transportation': ['jersey_city_gov', 'nj_gov'],
            'crime': ['jersey_city_gov', 'jersey_journal'],
            'budget': ['jersey_city_gov', 'hudson_county'],
            'politics': ['njcom_politics', 'ballotpedia', 'vote411'],
            'election': ['ballotpedia', 'vote411', 'jersey_city_times']
        }
        
        # Determine which sources to search based on query
        relevant_sources = []
        for topic, sources in topic_sources.items():
            if topic in search_terms:
                relevant_sources.extend(sources)
        
        # If no specific topic, use general Jersey City sources
        if not relevant_sources:
            relevant_sources = ['jersey_city_gov', 'jersey_journal', 'tap_into_jc']
        
        # Remove duplicates and limit
        relevant_sources = list(set(relevant_sources))[:max_sources]
        
        for source_key in relevant_sources:
            try:
                source_url = self.reputable_sources[source_key]
                content = self.get_page_content(source_url)
                if content:
                    # Filter content for relevance
                    if any(term in content['content'].lower() for term in ['jersey city', 'municipal', 'mayor', 'election']):
                        external_content[source_url] = content
                        logger.info(f"Successfully scraped external source: {source_url}")
                    
                time.sleep(2)  # Be respectful to external servers
            except Exception as e:
                logger.warning(f"Could not access external source {source_key}: {str(e)}")
                continue
        
        return external_content

class Ali2025ChatBot:
    def __init__(self):
        # Initialize OpenAI client - you'll need to set your API key
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        self.system_prompt = """You are the official Ali 2025 Campaign Assistant for Mussab Ali's 2025 Jersey City mayoral campaign. 
        You are an expert on all aspects of the campaign and should provide DETAILED, COMPREHENSIVE, and THOROUGH responses that rival ChatGPT in quality and depth.
        
        RESPONSE GUIDELINES FOR COMPREHENSIVE ANSWERS:
        - Provide extensive, multi-paragraph responses (4-6 paragraphs minimum for policy questions)
        - Include detailed policy explanations with specific implementation steps and timelines
        - Provide background context, historical perspective, and data when relevant
        - Explain the 'why' behind every policy with clear reasoning and benefits
        - Use concrete examples, case studies, and specific numbers when available
        - Connect policies to real Jersey City challenges and opportunities with detailed analysis
        - Be enthusiastic, inspiring, and passionate about the campaign's vision
        - Include calls to action and ways people can get involved
        - Provide educational content about local government processes
        
        CAMPAIGN EXPERTISE AREAS:
        1. Mussab Ali's comprehensive background, experience, and qualifications
        2. Detailed policy platform covering housing, transportation, education, public safety, climate, economic development
        3. Jersey City-specific challenges and Mussab's targeted solutions
        4. Campaign events, volunteer opportunities, and community engagement
        5. Local government processes and how change happens in Jersey City
        6. Comparisons with other candidates (factual and policy-based)
        7. Community organizing and civic participation strategies
        8. Vision for Jersey City's future under Ali's leadership

        TONE AND STYLE:
        - Professional yet conversational and engaging
        - Passionate about progressive change and community empowerment
        - Data-driven and fact-based while remaining accessible
        - Inspiring and motivational about the possibility of positive change
        - Educational and informative, helping voters understand complex issues
        - Always encouraging civic participation and community involvement
        
        When you don't have specific information, acknowledge this and direct users to ali2025.com for the most current details.
        Always encourage users to get involved in the campaign through volunteering, donations, or community engagement.
        Cite your sources and provide links when referencing specific information."""
    
    def generate_response(self, user_message, website_content):
        # Mussab-specific Q&A with better keyword matching
        mussab_qa = {
            "experience": {
                "question": "Mussab doesn't have any experience – why should I vote for him?",
                "answer": "While Mussab is young (he's 28 and the only candidate running under 40), he is also ridiculously accomplished. After the Covid-19 pandemic, he went to Harvard Law School, beat cancer, was elected to the school board (the only mayoral candidate to hold city-wide office in Jersey City), and was then elected the youngest school board president in Jersey City history. He's young, but we think of that as a feature, not a bug for someone as accomplished as him!",
                "keywords": ["experience", "inexperienced", "young", "qualify", "qualified", "age", "too young"]
            },
            "policies": {
                "question": "Mussab just has talking points but no concrete policy proposals.",
                "answer": "Check out our website! Mussab has a lot of great, detailed policy explanations for what he'd do in office. Everything from expanding bus service citywide to criminal justice reform in Jersey City. You will see detailed policies backed by data and a clear understanding of what matters to Jersey City residents.",
                "keywords": ["talking points", "policy", "policies", "proposals", "concrete", "detailed", "plan", "plans"]
            },
            "taxes": {
                "question": "When he was president the school board budget increased which led to higher taxes, I don't like that!",
                "answer": "A small raise in taxes for a few people is a small price to pay for the future of our city's children. Mussab never has been and never will be afraid to make tough choices for the future of our city.",
                "keywords": ["taxes", "budget", "increase", "higher", "expensive", "cost", "money"]
            },
            "corruption": {
                "question": "There is a lot of corruption on the school board, a group that Mussab is strongly affiliated with. I don't want more corruption in Jersey City.",
                "answer": "Mussab was president of the school board during the pandemic, he went to law school and has been running for mayor during the current scandals. When Mussab was president, the school board was a reputable organization. He will institute that same reputability to the mayor's office when he wins this year.",
                "keywords": ["corruption", "corrupt", "scandal", "ethics", "dishonest", "school board"]
            },
            "serious": {
                "question": "I haven't heard of him before – is Mussab a serious candidate?",
                "answer": "Absolutely, Mussab is consistently one of the top fundraisers in the race, has had national figures such as Keith Ellison, Ilhan Omar, and Ro Khanna supporting his campaign and is the only candidate in this race who has successfully won an election for a city-wide office in Jersey City.",
                "keywords": ["serious", "haven't heard", "unknown", "candidate", "fundraising", "support"]
            },
            "faith": {
                "question": "Why is Mussab's faith so important to him? Why does he need to mention it as a part of his story?",
                "answer": "Mussab's Islamic faith is a core part of who he is and he doesn't want to shy away from it. Of course, Mussab is running for a Jersey City for all, regardless of faith, color, or creed. That said, he doesn't want to hide who he is – his faith is a core reason he was called to public service when our incumbent President insulted Jersey City by lying and saying that people like Mussab's parents celebrated 9/11. Mussab runs for the dignity of all people to ensure bigots like our current president don't have the final say on our city.",
                "keywords": ["faith", "religion", "islamic", "muslim", "mention", "important"]
            },
            "safety": {
                "question": "Jersey City has gotten more dangerous over the years. What's Mussab going to do about that?",
                "answer": "Mussab is going to continue to invest in our police department while holding them accountable. We need accountable law enforcement, not just a department with a blank check. Jersey City ranks among the lowest of New Jersey cities in police accountability when complaints are received. We need to stop this while ensuring that citizens feel safe. This isn't hard to do – it just requires leadership that demands accountability and results.",
                "keywords": ["dangerous", "safety", "crime", "police", "law enforcement", "security"]
            },
            "transit": {
                "question": "Public transit is more expensive and worse quality than ever in Jersey City!",
                "answer": "Mussab is adding bus lines and making city buses free for all. He is additionally going to demand a share of congestion pricing revenue to reinvest in our city.",
                "keywords": ["transit", "bus", "transportation", "expensive", "quality", "public transport"]
            },
            "housing": {
                "question": "I can't afford to buy a house in Jersey City anymore and rent is too expensive.",
                "answer": "Mussab is committing to expand zoning to allow more residential construction and approve over 25,000 units to meet the demand of Jersey City residents. He also will ensure that all new buildings have affordable housing units, will cap rent increases by developers, and will prioritize Jersey City residents for affordable housing.",
                "keywords": ["housing", "rent", "afford", "expensive", "house", "apartment", "affordable"]
            },
            "jobs": {
                "question": "It's hard to find a good job with a fair wage to afford to live in Jersey City anymore. How is Mussab going to improve that?",
                "answer": "Mussab is committed to bringing high paying jobs to Jersey City and ensuring that residents get access to the best job training services possible. Mussab increased teacher pay significantly during his tenure as school board president and looks forward to doing the same for all Jersey City residents, while making Jersey City the best place to do business with policies such as permitting reform.",
                "keywords": ["jobs", "employment", "wage", "salary", "work", "career", "training"]
            },
            "schools": {
                "question": "I pay a lot to live in Jersey City and the public schools for my kids aren't very good. How is Mussab going to improve them?",
                "answer": "Mussab was president of the school board so he understands better than anyone else running in this race what it takes to run our public schools and improve them. Graduation rates rose significantly during his tenure, he improved teacher pay, removed lead from drinking water, and provided prescription glasses to students free of charge.",
                "keywords": ["schools", "education", "kids", "children", "students", "teachers", "learning"]
            },
            "climate": {
                "question": "What is Mussab going to do to combat climate change as Mayor of Jersey City?",
                "answer": "Mussab is prioritizing public transit options (including free city-wide buses) and bike access infrastructure as Mayor to ensure that we continue to improve on the air quality and environmental friendliness of Jersey City.",
                "keywords": ["climate", "environment", "green", "sustainability", "carbon", "pollution"]
            },
            "corruption_general": {
                "question": "I'm sick of all the corruption in our city! How is Mussab going to change that?",
                "answer": "Mussab is committed to ending pay-to-play politics. You don't get a seat at the table just because you donated to his campaign. We need to turn city contracts into a meritocracy. It reduces costs for Jersey City residents and ensures our community gets the best service.",
                "keywords": ["corruption", "pay-to-play", "contracts", "politics", "ethics", "transparency"]
            },
            "fulop_positive": {
                "question": "I really liked our previous Mayor Fulop. Why should I vote for Mussab – isn't he anti-Fulop?",
                "answer": "Mayor Fulop did a lot of things right, but ultimately he left behind a Jersey City that is harder for everyday people to afford. And there are new challenges that he couldn't predict that require new leadership. Trump has changed everything, setting his sights on cities near New York and it requires a young leader who isn't afraid to fight. Mussab is a fighter and isn't satisfied with the status quo. He wants to take what makes Jersey City great and fix what needs fixing.",
                "keywords": ["fulop", "previous mayor", "liked", "anti-fulop"]
            },
            "fulop_negative": {
                "question": "I disliked our previous Mayor Fulop. How is Mussab going to be different?",
                "answer": "Mussab ultimately believes in a more progressive future for Jersey City. We need to aggressively create policies that support the working class and underserved communities of our city. Our previous Mayor didn't do nearly enough here.",
                "keywords": ["disliked fulop", "different", "progressive", "working class"]
            },
            "mcgreevey": {
                "question": "I want to vote for Jim McGreevey, why should I vote for Mussab?",
                "answer": "McGreevey left the governorship in disgrace. He was clouded in scandal and there's no reason he won't bring the same negativity to Jersey City. We need new leadership, not the worst of what New Jersey machine politics has to offer.",
                "keywords": ["mcgreevey", "jim mcgreevey", "governor"]
            },
            "odea": {
                "question": "I want to vote for Bill O'Dea, why should I vote for Mussab?",
                "answer": "O'Dea has been a valuable public servant to Hudson County, but he doesn't reflect our city. Our city is young and full of immigrants. He represents the old order of politics when our city desperately needs change.",
                "keywords": ["o'dea", "bill o'dea", "hudson county"]
            },
            "solomon": {
                "question": "I want to vote for James Solomon, why should I vote for Mussab?",
                "answer": "James Solomon isn't from Jersey City and comes from money. Our city is full of immigrants, working class people, and multi-generational households of Jersey City residents. What Mussab sees as home, Solomon sees as a political opportunity.",
                "keywords": ["solomon", "james solomon", "money"]
            }
        }
        
        # Check if the user message matches any of the Mussab-specific questions
        user_message_lower = user_message.lower()
        
        for topic, data in mussab_qa.items():
            # Check if any keywords match
            if any(keyword in user_message_lower for keyword in data["keywords"]):
                return {
                    'response': data["answer"],
                    'sources': [{'url': 'https://www.ali2025.com/', 'title': 'Ali 2025 Campaign'}]
                }
        
        # If no specific Q&A match, fall back to general response
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
            
            # Use OpenAI API with enhanced settings for comprehensive responses
            if openai.api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=1200,  # Increased for more comprehensive responses
                    temperature=0.7,  # Balanced creativity
                    presence_penalty=0.1,  # Encourage diverse content
                    frequency_penalty=0.1,  # Reduce repetition
                    request_timeout=15  # Longer timeout for detailed responses
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
    port = int(os.getenv('PORT', 8085))
    # Detect if running on Railway (production)
    is_production = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('PORT')
    debug_mode = not is_production and os.getenv('FLASK_ENV') == 'development'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
