# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Environment
    app_env: str = "development"
    app_name: str = "video_pipeline_app"

    # Google API Key (used later for ADK)
    google_api_key: str = ""
    google_model_name: str = "gemini-2.5-flash"   # <-- ADD THIS
    GOOGLE_GENAI_USE_VERTEXAI: bool = False  # <-- ADD THIS

    # Logging
    log_level: str = "INFO"

    # 🔥 Pinecone + OpenAI (load directly using BaseSettings!)
    openai_api_key: str = ""
    pinecone_api_key: str = ""
    pinecone_env: str = ""     # e.g., "us-east-1"
    pinecone_index: str = "prompt-examples"

    # PostgreSQL (required)
    db_user: str
    db_password: str
    db_host: str
    db_name: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:5432/{self.db_name}"
        )
    
    # ⭐ NEW — For ADK session storage
    @property
    def adk_session_postgres_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:5432/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"  # silently ignore extra env values


settings = Settings()
