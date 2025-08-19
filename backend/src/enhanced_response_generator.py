"""
Enhanced Response Generator with O3-PRO Integration and Multilingual Support
Implements Step 2: Enhancement using O3 for empathetic, conversational responses
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from openai import OpenAI
from datetime import datetime
import os
from dataclasses import dataclass
from dotenv import load_dotenv

from knowledge_base import KnowledgeBaseManager, KnowledgeItem

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class ResponseContext:
    """Context information for generating responses"""
    user_query: str
    detected_language: str
    retrieved_facts: List[Tuple[KnowledgeItem, float]]
    confidence_threshold: float = 0.3
    max_response_length: int = 1500

class EnhancedResponseGenerator:
    """
    Enhanced response generator using O3-PRO for empathetic, conversational responses
    """
    
    def __init__(self, knowledge_base: KnowledgeBaseManager):
        self.kb = knowledge_base
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Available O3 models with pricing info
        self.o3_models = {
            'o3': {'cost_per_1m_tokens': 60.00, 'description': 'Premium O3 reasoning'},
            'o3-mini': {'cost_per_1m_tokens': 0.60, 'description': 'Cost-effective O3 reasoning'}
        }
        
        # Default to O3-mini for cost effectiveness, but allow override
        self.preferred_model = os.getenv('O3_MODEL', 'o3-mini')
        
        # Response templates for different languages
        self.response_templates = self._load_response_templates()
        
        # Empathy-first prompt engineering
        self.base_system_prompts = self._load_system_prompts()
        
        logger.info(f"Enhanced Response Generator initialized with O3 integration - using model: {self.preferred_model}")
    
    def _load_response_templates(self) -> Dict[str, Dict[str, str]]:
        """Load response templates for different languages and scenarios"""
        return {
            "en": {
                "acknowledgment": "I understand your concern about {topic}.",
                "empathy": "Many Jersey City residents share your feelings about this issue.",
                "explanation_intro": "Here's what's important to know:",
                "action_intro": "Mussab's track record shows:",
                "future_plan": "As mayor, his plan includes:",
                "closing": "Mussab believes Jersey City residents deserve {value}, and he's shown he'll fight for it."
            },
            "es": {
                "acknowledgment": "Entiendo tu preocupación sobre {topic}.",
                "empathy": "Muchos residentes de Jersey City comparten tus sentimientos sobre este tema.",
                "explanation_intro": "Esto es lo importante que debes saber:",
                "action_intro": "El historial de Mussab demuestra:",
                "future_plan": "Como alcalde, su plan incluye:",
                "closing": "Mussab cree que los residentes de Jersey City merecen {value}, y ha demostrado que luchará por ello."
            },
            "ar": {
                "acknowledgment": "أفهم قلقك بشأن {topic}.",
                "empathy": "العديد من سكان جيرسي سيتي يشاركونك مشاعرك حول هذه القضية.",
                "explanation_intro": "إليك ما هو مهم أن تعرفه:",
                "action_intro": "سجل مصعب يظهر:",
                "future_plan": "كعمدة، تشمل خطته:",
                "closing": "مصعب يؤمن أن سكان جيرسي سيتي يستحقون {value}، وقد أظهر أنه سيقاتل من أجل ذلك."
            },
            "fr": {
                "acknowledgment": "Je comprends votre préoccupation concernant {topic}.",
                "empathy": "Beaucoup de résidents de Jersey City partagent vos sentiments sur cette question.",
                "explanation_intro": "Voici ce qu'il est important de savoir :",
                "action_intro": "Le bilan de Mussab montre :",
                "future_plan": "En tant que maire, son plan comprend :",
                "closing": "Mussab croit que les résidents de Jersey City méritent {value}, et il a montré qu'il se battra pour cela."
            }
        }
    
    def _load_system_prompts(self) -> Dict[str, str]:
        """Load system prompts for different languages"""
        return {
            "en": """You are an expert AI assistant for Mussab Ali's 2025 Jersey City mayoral campaign. Your responses must follow this empathy-first structure:

1. ACKNOWLEDGE the voter's concern with genuine understanding
2. EXPLAIN the context and facts with clear reasoning  
3. SHOW Mussab's past actions and track record
4. CONNECT benefits to the voter's life and community
5. PRESENT future plans with specific details
6. CLOSE with values-based appeal

TONE GUIDELINES:
- Always start with empathy and acknowledgment
- Use conversational, accessible language  
- Be passionate but not defensive
- Include specific numbers, examples, and achievements
- Make it personal and relevant to Jersey City residents
- End with inspiring vision for the future

RESPONSE STRUCTURE EXAMPLE:
"I understand your frustration with [issue]. Many Jersey City families are dealing with this same challenge. Here's what's really happening: [context/facts]. Mussab's track record shows [specific actions/results]. This directly benefits you because [personal connection]. As mayor, his plan includes [specific future actions]. Mussab believes Jersey City should be a place where [values/vision]."

Keep responses comprehensive but conversational, roughly 200-400 words.""",

            "es": """Eres un asistente de IA experto para la campaña de alcalde de Mussab Ali 2025 en Jersey City. Tus respuestas deben seguir esta estructura centrada en la empatía:

1. RECONOCE la preocupación del votante con comprensión genuina
2. EXPLICA el contexto y los hechos con razonamiento claro
3. MUESTRA las acciones pasadas y el historial de Mussab  
4. CONECTA los beneficios con la vida del votante y la comunidad
5. PRESENTA planes futuros con detalles específicos
6. CIERRA con un llamado basado en valores

PAUTAS DE TONO:
- Siempre comienza con empatía y reconocimiento
- Usa lenguaje conversacional y accesible
- Sé apasionado pero no defensivo  
- Incluye números específicos, ejemplos y logros
- Hazlo personal y relevante para los residentes de Jersey City
- Termina con una visión inspiradora para el futuro

Mantén las respuestas comprehensivas pero conversacionales, aproximadamente 200-400 palabras.""",

            "ar": """أنت مساعد ذكي خبير لحملة مصعب علي 2025 لمنصب عمدة جيرسي سيتي. يجب أن تتبع ردودك هذه البنية المبنية على التعاطف:

1. اعترف بقلق الناخب مع فهم حقيقي
2. اشرح السياق والحقائق مع تفكير واضح
3. أظهر أعمال مصعب السابقة وسجله
4. اربط الفوائد بحياة الناخب والمجتمع
5. اقدم الخطط المستقبلية مع تفاصيل محددة
6. اختتم بنداء مبني على القيم

إرشادات النبرة:
- ابدأ دائماً بالتعاطف والاعتراف
- استخدم لغة محادثة ومفهومة
- كن شغوفاً وليس دفاعياً
- اشمل أرقام وأمثلة وإنجازات محددة
- اجعلها شخصية وذات صلة بسكان جيرسي سيتي
- انته برؤية ملهمة للمستقبل

حافظ على الردود شاملة ولكن محادثة، حوالي 200-400 كلمة.""",

            "fr": """Vous êtes un assistant IA expert pour la campagne de maire de Mussab Ali 2025 à Jersey City. Vos réponses doivent suivre cette structure centrée sur l'empathie :

1. RECONNAISSEZ la préoccupation de l'électeur avec une compréhension genuine
2. EXPLIQUEZ le contexte et les faits avec un raisonnement clair
3. MONTREZ les actions passées et le bilan de Mussab
4. CONNECTEZ les avantages à la vie de l'électeur et à la communauté  
5. PRÉSENTEZ les plans futurs avec des détails spécifiques
6. TERMINEZ avec un appel basé sur les valeurs

DIRECTIVES DE TON :
- Commencez toujours par l'empathie et la reconnaissance
- Utilisez un langage conversationnel et accessible
- Soyez passionné mais pas défensif
- Incluez des chiffres spécifiques, des exemples et des réalisations
- Rendez-le personnel et pertinent pour les résidents de Jersey City
- Terminez par une vision inspirante pour l'avenir

Gardez les réponses complètes mais conversationnelles, environ 200-400 mots."""
        }
    
    def generate_response(self, context: ResponseContext) -> Dict[str, Any]:
        """
        Generate an empathetic, conversational response using O3-PRO
        """
        try:
            # Step 1: Analyze the retrieved facts
            relevant_facts = self._filter_relevant_facts(context)
            
            if not relevant_facts:
                return self._generate_fallback_response(context)
            
            # Step 2: Prepare context for O3-PRO
            facts_summary = self._prepare_facts_summary(relevant_facts, context.detected_language)
            
            # Step 3: Generate response using O3-PRO
            enhanced_response = self._generate_with_o3_pro(context, facts_summary)
            
            # Step 4: Post-process and validate response
            final_response = self._post_process_response(enhanced_response, context)
            
            return {
                'response': final_response,
                'language': context.detected_language,
                'confidence_score': self._calculate_confidence_score(context, relevant_facts),
                'sources': [item.sources[0].to_dict() for item, _ in relevant_facts[:3]],
                'topics_covered': list(set([item.topic for item, _ in relevant_facts])),
                'response_type': 'enhanced_o3_pro'
            }
            
        except Exception as e:
            logger.error(f"Error generating enhanced response: {str(e)}")
            return self._generate_fallback_response(context)
    
    def _filter_relevant_facts(self, context: ResponseContext) -> List[Tuple[KnowledgeItem, float]]:
        """Filter and rank facts by relevance"""
        relevant_facts = []
        
        for item, score in context.retrieved_facts:
            if score >= context.confidence_threshold:
                relevant_facts.append((item, score))
        
        # Sort by score and limit to top 5 most relevant facts
        relevant_facts.sort(key=lambda x: x[1], reverse=True)
        return relevant_facts[:5]
    
    def _prepare_facts_summary(self, facts: List[Tuple[KnowledgeItem, float]], language: str) -> str:
        """Prepare a structured summary of facts for the AI model"""
        if not facts:
            return "No specific information available."
        
        summary_parts = []
        
        # Group facts by topic
        topics = {}
        for item, score in facts:
            if item.topic not in topics:
                topics[item.topic] = []
            topics[item.topic].append((item, score))
        
        for topic, topic_facts in topics.items():
            summary_parts.append(f"\n=== {topic.upper()} ===")
            for item, score in topic_facts:
                credibility = item.sources[0].credibility.value if item.sources else "unknown"
                summary_parts.append(f"[Confidence: {score:.2f}, Source: {credibility}]")
                summary_parts.append(item.content)
                summary_parts.append("")
        
        return "\n".join(summary_parts)
    
    def _generate_with_o3_pro(self, context: ResponseContext, facts_summary: str) -> str:
        """Generate response using OpenAI O3 model with advanced reasoning"""
        
        # Select appropriate system prompt based on language
        system_prompt = self.base_system_prompts.get(context.detected_language, self.base_system_prompts["en"])
        
        # Create comprehensive context message optimized for O3 reasoning
        context_message = f"""
VOTER QUESTION: {context.user_query}
DETECTED LANGUAGE: {context.detected_language}

RELEVANT CAMPAIGN INFORMATION:
{facts_summary}

RESPONSE REQUIREMENTS:
- Respond in {context.detected_language}
- Follow the empathy-first structure: acknowledge → explain → show action → connect benefits → future plan
- Use specific facts and numbers from the provided information
- Keep response conversational and between 200-400 words
- Make it personally relevant to Jersey City residents
- Include Mussab's track record and future plans
- End with an inspiring, values-based message
- Think through your reasoning step by step for the most empathetic and effective response
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context_message}
        ]
        
        try:
            # Try O3 model first (premium reasoning)
            logger.info(f"Using O3 model: {self.preferred_model}")
            response = self.openai_client.chat.completions.create(
                model=self.preferred_model,
                messages=messages,
                max_completion_tokens=600,  # O3 models use max_completion_tokens
                # Note: O3 models don't support temperature, presence_penalty, etc.
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.warning(f"O3 model {self.preferred_model} failed: {str(e)}, falling back to O1")
            
            # Fallback to O1-mini if O3 fails
            try:
                response = self.openai_client.chat.completions.create(
                    model="o1-mini",
                    messages=messages
                )
                return response.choices[0].message.content.strip()
                
            except Exception as e2:
                logger.warning(f"O1 fallback failed: {str(e2)}, using GPT-4")
                
                # Final fallback to GPT-4
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages,
                    max_tokens=600,
                    temperature=0.7
                )
                
                return response.choices[0].message.content.strip()
    
    def _post_process_response(self, response: str, context: ResponseContext) -> str:
        """Post-process the generated response for quality and consistency"""
        
        # Ensure response is not too long
        if len(response) > context.max_response_length:
            # Truncate at sentence boundary
            sentences = response.split('. ')
            truncated = []
            current_length = 0
            
            for sentence in sentences:
                if current_length + len(sentence) + 2 <= context.max_response_length:
                    truncated.append(sentence)
                    current_length += len(sentence) + 2
                else:
                    break
            
            response = '. '.join(truncated)
            if response and not response.endswith('.'):
                response += '.'
        
        # Ensure proper language consistency
        if context.detected_language != 'en' and 'Mussab' not in response:
            # Add candidate name if missing in non-English responses
            response = response.replace('the candidate', 'Mussab')
            response = response.replace('he ', 'Mussab ')
        
        return response
    
    def _calculate_confidence_score(self, context: ResponseContext, facts: List[Tuple[KnowledgeItem, float]]) -> float:
        """Calculate overall confidence score for the response"""
        if not facts:
            return 0.1
        
        # Average of fact scores weighted by source credibility
        total_score = 0
        total_weight = 0
        
        for item, score in facts:
            credibility_weight = {
                'primary': 1.0,
                'verified': 0.8,
                'secondary': 0.6,
                'unverified': 0.3
            }.get(item.sources[0].credibility.value if item.sources else 'unverified', 0.3)
            
            total_score += score * credibility_weight
            total_weight += credibility_weight
        
        if total_weight == 0:
            return 0.1
        
        return min(total_score / total_weight, 1.0)
    
    def _generate_fallback_response(self, context: ResponseContext) -> Dict[str, Any]:
        """Generate a fallback response when no relevant facts are found"""
        
        fallback_responses = {
            "en": "Thank you for your question about Mussab Ali's campaign. While I don't have specific information about that topic in my current knowledge base, I encourage you to visit ali2025.com for the most comprehensive and up-to-date information about Mussab's policies and positions. You can also contact the campaign directly to get detailed answers to your questions. Mussab is committed to being accessible to all Jersey City residents and addressing their concerns.",
            
            "es": "Gracias por tu pregunta sobre la campaña de Mussab Ali. Aunque no tengo información específica sobre ese tema en mi base de conocimientos actual, te animo a visitar ali2025.com para obtener la información más completa y actualizada sobre las políticas y posiciones de Mussab. También puedes contactar directamente con la campaña para obtener respuestas detalladas a tus preguntas. Mussab está comprometido a ser accesible a todos los residentes de Jersey City y abordar sus preocupaciones.",
            
            "ar": "شكراً لك على سؤالك حول حملة مصعب علي. بينما لا أملك معلومات محددة حول هذا الموضوع في قاعدة معرفتي الحالية، أشجعك على زيارة ali2025.com للحصول على أشمل المعلومات وأحدثها حول سياسات مصعب ومواقفه. يمكنك أيضاً التواصل مع الحملة مباشرة للحصول على إجابات مفصلة لأسئلتك. مصعب ملتزم بأن يكون في متناول جميع سكان جيرسي سيتي ومعالجة مخاوفهم.",
            
            "fr": "Merci pour votre question sur la campagne de Mussab Ali. Bien que je n'aie pas d'informations spécifiques sur ce sujet dans ma base de connaissances actuelle, je vous encourage à visiter ali2025.com pour obtenir les informations les plus complètes et à jour sur les politiques et positions de Mussab. Vous pouvez également contacter directement la campagne pour obtenir des réponses détaillées à vos questions. Mussab s'engage à être accessible à tous les résidents de Jersey City et à répondre à leurs préoccupations."
        }
        
        language = context.detected_language
        fallback_text = fallback_responses.get(language, fallback_responses["en"])
        
        return {
            'response': fallback_text,
            'language': language,
            'confidence_score': 0.1,
            'sources': [],
            'topics_covered': [],
            'response_type': 'fallback'
        }

def create_test_scenario():
    """Create a test scenario to demonstrate the enhanced response generator"""
    from data_loader import CampaignDataLoader
    
    # Initialize knowledge base and load data
    kb = KnowledgeBaseManager("test_enhanced_kb.db")
    loader = CampaignDataLoader(kb)
    loader.load_all_data()
    
    # Initialize response generator
    generator = EnhancedResponseGenerator(kb)
    
    # Test queries in different languages
    test_queries = [
        {
            "query": "When Mussab was school board president the budget went up and my taxes did too — I don't like that.",
            "language": "en"
        },
        {
            "query": "¿Por qué debería votar por Mussab si es tan joven?",
            "language": "es"
        },
        {
            "query": "What's Mussab going to do about housing costs?",
            "language": "en"
        },
        {
            "query": "How will he make transportation better?",
            "language": "en"
        }
    ]
    
    print("\n" + "="*80)
    print("TESTING ENHANCED RESPONSE GENERATOR WITH O3-PRO")
    print("="*80)
    
    for test_case in test_queries:
        print(f"\n{'='*50}")
        print(f"QUERY: {test_case['query']}")
        print(f"LANGUAGE: {test_case['language']}")
        print(f"{'='*50}")
        
        # Search for relevant facts
        retrieved_facts = kb.search_knowledge(test_case['query'], test_case['language'], limit=10)
        
        # Create response context
        context = ResponseContext(
            user_query=test_case['query'],
            detected_language=test_case['language'],
            retrieved_facts=retrieved_facts
        )
        
        # Generate enhanced response
        result = generator.generate_response(context)
        
        print(f"\nRESPONSE:")
        print(result['response'])
        print(f"\nMETADATA:")
        print(f"- Confidence Score: {result['confidence_score']:.3f}")
        print(f"- Response Type: {result['response_type']}")
        print(f"- Topics Covered: {', '.join(result['topics_covered'])}")
        print(f"- Sources: {len(result['sources'])} sources")

if __name__ == "__main__":
    create_test_scenario()
