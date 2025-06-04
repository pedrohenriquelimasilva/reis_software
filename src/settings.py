from dotenv import dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

config = dotenv_values(dotenv_path=".env")
