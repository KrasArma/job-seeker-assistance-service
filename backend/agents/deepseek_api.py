import requests
import json
from typing import Dict, Any, Optional, Union
from config.config_reader import config_reader
from config.data_models import DeepseekConfig
from .modules.response_types import ResponseStatus, ResponseType, BaseResponseHandler

class DeepseekClient:
    """
    Client for interacting with Deepseek API via OpenRouter.
    Only responsible for API calls. Uses BaseResponseHandler for formatting.
    """
    def __init__(self):
        self.config = config_reader.get(DeepseekConfig)
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.config.deepseek}",
            "Content-Type": "application/json"
        }
        self.base_payload = {
            "model": self.config.model_name,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "frequency_penalty": self.config.frequency_penalty,
            "presence_penalty": self.config.presence_penalty
        }
        self.response_handler = BaseResponseHandler()

    def _make_request(self, messages: list) -> Union[str, None]:
        payload = self.base_payload.copy()
        payload["messages"] = messages
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return None
        except Exception:
            return None

    def send_prompt(self, prompt: str, request_id: Optional[str] = None) -> Dict[str, Any]:
        messages = [{"role": "user", "content": prompt}]
        try:
            content = self._make_request(messages)
            if content:
                return self.response_handler.handle(ResponseType.TEXT, content, request_id, prompt)
            else:
                return self.response_handler.handle(ResponseType.ERROR, None, request_id, prompt, error=Exception("No response from API"))
        except Exception as e:
            return self.response_handler.handle(ResponseType.ERROR, None, request_id, prompt, error=e)

    def send_prompt_with_json_response(self, prompt: str, request_id: Optional[str] = None) -> Dict[str, Any]:
        messages = [{"role": "user", "content": prompt}]
        try:
            content = self._make_request(messages)
            if content:
                try:
                    response_json = json.loads(content)
                    return self.response_handler.handle(ResponseType.JSON, response_json, request_id, prompt)
                except Exception as e:
                    return self.response_handler.handle(ResponseType.ERROR, None, request_id, prompt, error=e)
            else:
                return self.response_handler.handle(ResponseType.ERROR, None, request_id, prompt, error=Exception("No response from API"))
        except Exception as e:
            return self.response_handler.handle(ResponseType.ERROR, None, request_id, prompt, error=e)

