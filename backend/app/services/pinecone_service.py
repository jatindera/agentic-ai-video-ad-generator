# app/services/pinecone_service.py

import logging
from typing import List, Optional, Dict, Any

from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings

logger = logging.getLogger("backend")


class PineconeService:
    def __init__(self):
        logger.info("🔵 Initializing Pinecone client...")

        if not settings.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY is not set")

        # Create Pinecone client
        self.pc = Pinecone(api_key=settings.pinecone_api_key)

        # Ensure index exists
        existing = [idx["name"] for idx in self.pc.list_indexes()]

        if settings.pinecone_index not in existing:
            logger.info(f"🟦 [PINECONE] Creating index {settings.pinecone_index}...")
            self.pc.create_index(
                name=settings.pinecone_index,
                dimension=3072,   # OpenAI text-embedding-3-large
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1",
                ),
            )
        else:
            logger.info(f"🟩 [PINECONE] Using existing index: {settings.pinecone_index}")

        # Index instance
        self.index = self.pc.Index(settings.pinecone_index)

    # ------------------------------------------------------------
    # UPSERT
    # ------------------------------------------------------------
    async def upsert_example(
        self,
        example_id: str,
        embedding: List[float],
        metadata: Dict[str, Any],
    ) -> None:

        logger.info(f"🟦 [PINECONE] Upserting ID={example_id}")
        logger.info(f"Embedding size = {len(embedding)}")

        self.index.upsert(
            vectors=[
                {
                    "id": example_id,
                    "values": embedding,
                    "metadata": metadata,
                }
            ]
        )

        logger.info("🟩 [PINECONE] Upsert successful")

    # ------------------------------------------------------------
    # QUERY EXAMPLES (semantic + metadata filtering)
    # ------------------------------------------------------------
    async def query_examples(
        self,
        embedding: List[float],
        top_k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ):
        """
        metadata_filter may contain:
        {
            "business_type": "...",
            "ad_style": "...",
            "tone": "...",
            "target_audience": "...",
            "tags": {"$in": [...]}
        }
        """

        logger.info(
            f"🟦 [PINECONE] Query top_k={top_k}, filter={metadata_filter or None}"
        )

        result = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            filter=metadata_filter or None,
        )

        return result.matches


pinecone_service = PineconeService()
