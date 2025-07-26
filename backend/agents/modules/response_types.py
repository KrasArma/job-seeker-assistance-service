from enum import Enum
from typing import Dict, Any, Optional

class ResponseStatus(Enum):
    """Standard response statuses"""
    DONE = "DONE"
    FAIL = "FAIL"

class ResponseType(Enum):
    """Standard response types"""
    TEXT = "text"
    JSON = "json"
    ERROR = "error"
    DEFAULT = "default"

class BaseResponseHandler:
    """
    Base response handler with standard formatting methods.
    """
    def __init__(self):
        self.response_map = {
            ResponseType.TEXT: self._format_text_response,
            ResponseType.JSON: self._format_json_response,
            ResponseType.ERROR: self._format_error_response,
            ResponseType.DEFAULT: self._format_default_response
        }

    def handle(self, response_type: ResponseType, raw: Any, request_id: Optional[str], prompt: Optional[str], error: Optional[Exception] = None) -> Dict[str, Any]:
        handler = self.response_map.get(response_type, self.response_map[ResponseType.DEFAULT])
        return handler(raw, request_id, prompt, error)

    def _format_text_response(self, raw: Any, request_id: Optional[str], prompt: Optional[str], error: Optional[Exception] = None) -> Dict[str, Any]:
        return {
            "request_id": request_id,
            "status": ResponseStatus.DONE.value if raw else ResponseStatus.FAIL.value,
            "response": raw,
            "prompt": prompt
        } if raw else self._format_error_response(raw, request_id, prompt, Exception("No response from API"))

    def _format_json_response(self, raw: Any, request_id: Optional[str], prompt: Optional[str], error: Optional[Exception] = None) -> Dict[str, Any]:
        return {
            "request_id": request_id,
            "status": ResponseStatus.DONE.value,
            "response": raw,
            "prompt": prompt
        } if isinstance(raw, dict) else self._format_error_response(raw, request_id, prompt, Exception("Invalid JSON response"))

    def _format_error_response(self, raw: Any, request_id: Optional[str], prompt: Optional[str], error: Optional[Exception] = None) -> Dict[str, Any]:
        return {
            "request_id": request_id,
            "status": ResponseStatus.FAIL.value,
            "message": str(error) if error else "Unknown error",
            "prompt": prompt
        }

    def _format_default_response(self, raw: Any, request_id: Optional[str], prompt: Optional[str], error: Optional[Exception] = None) -> Dict[str, Any]:
        return {
            "request_id": request_id,
            "status": ResponseStatus.DONE.value if raw else ResponseStatus.FAIL.value,
            "data": raw,
            "prompt": prompt
        } 