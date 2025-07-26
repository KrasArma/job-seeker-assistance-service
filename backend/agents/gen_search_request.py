import re
from typing import Dict, Any, Optional, List
from backend.agents.deepseek_api import DeepseekClient
from .modules.response_types import ResponseStatus
from config.config_reader import config_reader
from config.data_models import SearchAgentPromptsConfig


class SearchRequestAgent:
    """
    Agent for generating search queries based on natural language
    Supports Russian and English languages
    """
    
    def __init__(self):
        """Initialize agent with prompts from configuration"""
        self.deepseek = DeepseekClient()
        self.prompts = config_reader.get_prompts("search_agent")
    
    def _detect_language(self, text: str) -> str:
        """
        Detects text language (simple heuristic)
        
        Args:
            text: Text to detect language for
            
        Returns:
            'ru' for Russian, 'en' for English
        """
        cyrillic_chars = sum(1 for char in text if '\u0400' <= char <= '\u04FF')
        if cyrillic_chars > len(text) * 0.3:  
            return 'ru'
        else:
            return 'en'
    
    def nl_to_hh_query(self, user_text: str) -> str:
        """
        Translates user query in natural language to hh.ru search query.
        Uses LLM (DeepSeek) to generate correct search expression.
        
        Args:
            user_text: User query in natural language
            
        Returns:
            Search query for hh.ru
        """
        prompt = self.prompts.nl_to_hh_query.format(
            syntax=self.prompts.hh_query_syntax,
            user_text=user_text
        )
        
        result = self.deepseek.send_prompt(prompt)
        if result["status"] == ResponseStatus.DONE.value and result.get("response"):
            hh_query = result["response"]
        else:
            hh_query = user_text
            
        hh_query = re.sub(r'\s+', ' ', hh_query).strip()
        return hh_query
    
    def generate_multilingual_queries(self, user_text: str) -> Dict[str, List[str]]:
        """
        Generates search queries in Russian and English languages
        
        Args:
            user_text: User query
            
        Returns:
            Dictionary with queries in both languages
        """
        detected_lang = self._detect_language(user_text)
        
        prompts_map = {
            'ru': self.prompts.multilingual_queries_ru,
            'en': self.prompts.multilingual_queries_en
        }
        
        prompt = prompts_map[detected_lang].format(user_text=user_text)
        result = self.deepseek.send_prompt(prompt)
        
        if result["status"] == ResponseStatus.DONE.value and result.get("response"):
            generated_queries = [q.strip() for q in result["response"].split('\n') if q.strip()]
        else:
            generated_queries = []
        
        response_map = {
            'ru': {
                "original_language": "ru",
                "original_query": user_text,
                "russian_queries": [user_text],
                "english_queries": generated_queries
            },
            'en': {
                "original_language": "en",
                "original_query": user_text,
                "russian_queries": generated_queries,
                "english_queries": [user_text]
            }
        }
        
        return response_map[detected_lang]
    
    def query_to_filter(self, query: str) -> Dict[str, Any]:
        """
        Converts user query to structured filter for job search
        
        Args:
            query: User query
            
        Returns:
            Structured filter as dictionary
        """
        prompt = self.prompts.query_to_filter.format(query=query)
        
        result = self.deepseek.send_prompt_with_json_response(prompt)
        if result["status"] == ResponseStatus.DONE.value and result.get("response"):
            return result["response"]
        else:
            return {"text": query}
    
    def query_to_filter_multilingual(self, query: str) -> Dict[str, Any]:
        """
        Converts user query to structured filter with multilingual support
        
        Args:
            query: User query
            
        Returns:
            Structured filter with variants in both languages
        """
        base_filter = self.query_to_filter(query)
        multilingual_queries = self.generate_multilingual_queries(query)

        base_filter.update({
            "multilingual_queries": multilingual_queries,
            "original_language": multilingual_queries["original_language"]
        })
        
        return base_filter
    
    def analyze_vacancy(self, vacancy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes vacancy and returns structured information
        
        Args:
            vacancy_data: Vacancy data
            
        Returns:
            Vacancy analysis
        """
        prompt = self.prompts.analyze_vacancy.format(vacancy_data=vacancy_data)
        
        result = self.deepseek.send_prompt_with_json_response(prompt)
        if result["status"] == ResponseStatus.DONE.value and result.get("response"):
            return result["response"]
        else:
            return {"match_score": 0}
    
    def generate_search_suggestions(self, user_query: str) -> Dict[str, Any]:
        """
        Generates search improvement suggestions with multilingual support
        
        Args:
            user_query: User query
            
        Returns:
            Search suggestions in both languages
        """
        detected_lang = self._detect_language(user_query)
        
        prompts_map = {
            'ru': self.prompts.search_suggestions_ru,
            'en': self.prompts.search_suggestions_en
        }
        
        prompt = prompts_map[detected_lang].format(user_query=user_query)
        result = self.deepseek.send_prompt_with_json_response(prompt)
        
        if result["status"] == ResponseStatus.DONE.value and result.get("response"):
            return result["response"]
        else:
            return {
                "alternative_queries_ru": [user_query] if detected_lang == 'ru' else [],
                "alternative_queries_en": [user_query] if detected_lang == 'en' else []
            }


