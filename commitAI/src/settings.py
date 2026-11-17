from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', env_prefix='GEMINI_'
    )

    API_KEY: SecretStr
    MODELO: str
    THINKING_LEVEL: str
    MAX_TOKENS: int
