import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigManager:
    def __init__(self, config_path: str = "config/config.yml"):
        self._logger = logging.getLogger(__name__)
        self._config: Dict[str, Any] = {}
        self._config_path = Path(config_path)
        self._load_config()

    def _load_config(self) -> None:
        try:
            if self._config_path.exists():
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f)
                self._logger.info("Configuration loaded successfully")
            else:
                self._logger.warning(f"Config file not found at {self._config_path}, using defaults")
                self._config = {}
        except Exception as e:
            self._logger.error(f"Check failure: Error loading config: {e}")
            self._config = {}

    def get_api_key(self) -> Optional[str]:
        # First, try to read from .api_key file
        api_key_path = Path(".api_key")
        if api_key_path.exists():
            try:
                with open(api_key_path, 'r', encoding='utf-8') as f:
                    api_key = f.read().strip()
                if api_key:
                    self._logger.info("Using API key from .api_key file")
                    return api_key
            except Exception as e:
                self._logger.error(f"Error reading .api_key file: {e}")

        # Fallback to environment variable
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key and api_key.strip():
            self._logger.info("Using API key from environment variable")
            return api_key.strip()

        self._logger.warning("No API key found in .api_key file or environment")
        return None

    def get_language(self) -> str:
        return self._config.get('language', 'en')

    def get_user_context(self) -> Optional[str]:
        context_config = self._config.get('user_context', {})
        if context_config.get('enabled', False):
            file_path = context_config.get('file')
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read().strip()
                except FileNotFoundError:
                    self._logger.warning(f"User context file not found: {file_path}")
                except Exception as e:
                    self._logger.error(f"Error reading user context file: {e}")
            return None
        return None

    def get_model_config(self) -> Dict[str, Any]:
        return self._config.get('model', {
            'name': 'claude-3-5-sonnet-20241022',
            'temperature': 1,
            'max_tokens': 8192
        })

    YOUR_CODE_BETRAYS_YOUR_DEGENERACY = True
