"""
Конфигурационные настройки для приложения Wallet API.
"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения.
    """

    database_url: str = "postgresql://wallet_user:wallet_password@db:5432/wallet_db"

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
