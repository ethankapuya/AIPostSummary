from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

load_dotenv()

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    MAX_IMAGE_SIZE_MB: int = 5
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def MAX_IMAGE_SIZE_BYTES(self) -> int:
        return self.MAX_IMAGE_SIZE_MB * 1024 * 1024

settings = Settings(ANTHROPIC_API_KEY=str(os.getenv("ANTHROPIC_API_KEY")))

# re-export flat for convenience
ANTHROPIC_API_KEY = settings.ANTHROPIC_API_KEY
MAX_IMAGE_SIZE_MB = settings.MAX_IMAGE_SIZE_MB
MAX_IMAGE_SIZE_BYTES = settings.MAX_IMAGE_SIZE_BYTES