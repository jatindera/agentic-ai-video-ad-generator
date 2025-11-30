from pydantic_settings import BaseSettings

class Settings(BaseSettings):
     # Google API Key (used later for ADK)
    google_api_key: str = ""
    GOOGLE_GENAI_USE_VERTEXAI: bool = False  # <-- ADD THIS
    
    class Config:
        env_file = ".env"

settings = Settings()
