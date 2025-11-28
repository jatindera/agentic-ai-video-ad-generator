from openai import OpenAI
from app.core.config import settings
from typing import List
import logging

logger = logging.getLogger("backend")

# Initialize OpenAI client
client = OpenAI(api_key=settings.openai_api_key)

EMBED_MODEL = "text-embedding-3-large"


class EmbeddingService:
    """Wrapper around OpenAI embeddings with unified async API."""

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI API.
        """
        try:
            if not text or not text.strip():
                raise ValueError("Text for embedding is empty.")

            logger.info("Generating embedding via OpenAI...")

            response = client.embeddings.create(
                model=EMBED_MODEL,
                input=text
            )

            embedding = response.data[0].embedding
            return embedding

        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise

    # Alias for backward compatibility
    async def get_embedding(self, text: str) -> List[float]:
        return await self.generate_embedding(text)


# Singleton instance
embedding_service = EmbeddingService()
