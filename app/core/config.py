from pydantic import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str | None = None
    BING_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
