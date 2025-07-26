import yaml
import os
from typing import Type, TypeVar, Any, Dict
from .data_models import DatabaseConfig, HHConfig, DeepseekConfig, SearchAgentPromptsConfig
from custom_logger import logger

T = TypeVar('T')

class ConfigReader:
    def __init__(self):
        method = "ConfigReader.__init__"
        logger.info(f"{method} called")
        try:
            base_dir = os.path.dirname(__file__)
            config_path = os.path.join(base_dir, 'config-modules.yaml')
            with open(config_path, 'r', encoding='utf-8') as f:
                self._raw = yaml.safe_load(f)["configurations"]
            logger.info(f"{method} finished, loaded keys: {list(self._raw.keys())}")
        except Exception as e:
            logger.error("ConfigError", str(e), method=method)
            raise

    def get(self, key_or_class: Any, cls: Type[T] = None) -> T:
        method = "ConfigReader.get"
        logger.info(f"{method} called, key_or_class={key_or_class}, cls={cls}")
        try:
            if isinstance(key_or_class, str):
                key = key_or_class
                if cls is None:
                    raise ValueError("If a key is provided, a class must also be provided")
            else:
                cls = key_or_class
                key = cls.__name__.replace('Config', '').lower()
            if key not in self._raw:
                raise Exception(f"{key} not found in config")
            result = cls.from_dict(self._raw[key])
            logger.info(f"{method} finished, key={key}")
            return result
        except Exception as e:
            logger.error("ConfigError", str(e), input_data={"key_or_class": key_or_class, "cls": cls}, method=method)
            raise

    def get_prompts(self, agent_name: str = "search_agent") -> SearchAgentPromptsConfig:
        """
        Loads prompts configuration for specified agent
        
        Args:
            agent_name: Name of the agent (default: "search_agent")
            
        Returns:
            SearchAgentPromptsConfig with loaded prompts
        """
        method = "ConfigReader.get_prompts"
        logger.info(f"{method} called, agent_name={agent_name}")
        try:
            base_dir = os.path.dirname(__file__)
            prompts_path = os.path.join(base_dir, 'prompts.yaml')
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts_data = yaml.safe_load(f)["prompts"][agent_name]
            
            result = SearchAgentPromptsConfig.from_dict(prompts_data)
            logger.info(f"{method} finished, agent_name={agent_name}")
            return result
        except Exception as e:
            logger.error("PromptsConfigError", str(e), input_data={"agent_name": agent_name}, method=method)
            raise

config_reader = ConfigReader() 