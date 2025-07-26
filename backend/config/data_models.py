from dataclasses import dataclass, fields
from typing import Any, Type, TypeVar, Dict, NoReturn

T = TypeVar('T')

@dataclass
class DatabaseConfig:
    url: str
    echo: bool = True
    user: str = "hhuser"
    password: str = "hhpassword"
    host: str = "db"
    port: int = 5432
    dbname: str = "hhdb"
    pool_size: int = 5
    pool_size_overflow: int = 10

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        cls._check_config(data)
        return cls(**data)

    @classmethod
    def _check_config(cls, data: Dict[str, Any]) -> NoReturn:
        for f in fields(cls):
            if f.name not in data:
                raise Exception(f"{f.name} not found in config for {cls.__name__}")

@dataclass
class HHConfig:
    api_url: str
    user_agent: str
    token: str = ""

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        cls._check_config(data)
        return cls(**data)

    @classmethod
    def _check_config(cls, data: Dict[str, Any]) -> NoReturn:
        for f in fields(cls):
            if f.name not in data:
                raise Exception(f"{f.name} not found in config for {cls.__name__}")

@dataclass
class DeepseekConfig:
    model_name: str
    max_tokens: int
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    deepseek: str

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        cls._check_config(data)
        return cls(**data)

    @classmethod
    def _check_config(cls, data: Dict[str, Any]) -> NoReturn:
        for f in fields(cls):
            if f.name not in data:
                raise Exception(f"{f.name} not found in config for {cls.__name__}")

@dataclass
class SearchAgentPromptsConfig:
    hh_query_syntax: str
    nl_to_hh_query: str
    multilingual_queries_ru: str
    multilingual_queries_en: str
    query_to_filter: str
    analyze_vacancy: str
    search_suggestions_ru: str
    search_suggestions_en: str

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        cls._check_config(data)
        return cls(**data)

    @classmethod
    def _check_config(cls, data: Dict[str, Any]) -> NoReturn:
        for f in fields(cls):
            if f.name not in data:
                raise Exception(f"{f.name} not found in config for {cls.__name__}") 