# app/services/retrieval_service.py

from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.example_service import example_service
import logging
from app.schemas.retrieval_schema import (
    RetrievalPreferences,
    RetrievedExample,
)

logger = logging.getLogger("backend")


class ExampleRetrievalService:
    """
    High-level retrieval service used by agents.

    Responsibilities:
    - Turn business description into an embedding (via example_service internally)
    - Query Pinecone for similar examples
    - Fetch full records from Postgres
    - Re-rank based on category, tones, region
    """

    async def get_examples_for_business(
        self,
        db: AsyncSession,
        business_description: str,
        preferences: RetrievalPreferences,
    ) -> List[RetrievedExample]:
        """
        Main entrypoint for agents.

        Args:
            db: Async SQLAlchemy session
            business_description: rich text describing the business
            preferences: category/tone/region preferences

        Returns:
            A list of re-ranked RetrievedExample objects.
        """

        if not business_description or not business_description.strip():
            raise ValueError("business_description cannot be empty")

        # 🔹 Step 1: Use existing search service to get base results from Pinecone + Postgres
        logger.info(
            "🔎 [RETRIEVAL] Searching examples for business (category=%s, tones=%s, region=%s)",
            preferences.category,
            preferences.tones,
            preferences.region,
        )

        base_results = await example_service.search_examples(
            db=db,
            query=business_description,
            top_k=preferences.max_examples * 2,  # fetch a bit more for re-ranking
            category=preferences.category,
        )

        if not base_results:
            logger.warning("⚠️ [RETRIEVAL] No examples found for query.")
            return []

        # 🔹 Step 2: Re-rank according to tones + region + category
        re_ranked: List[RetrievedExample] = []

        tones_lower = {t.lower().strip() for t in preferences.tones} if preferences.tones else set()
        region_lower = preferences.region.lower().strip() if preferences.region else None
        category_lower = preferences.category.lower().strip() if preferences.category else None

        for res in base_results:
            # `res` is assumed to be a dict from example_service.search_examples
            # with keys: id, title, content, category, tags, score
            base_score = float(res.score)
            category = res.category
            tags = res.tags or []

            tags_lower = {str(t).lower().strip() for t in tags}

            # Start with Pinecone similarity score
            final_score = base_score

            # ✅ Category boost
            if category_lower and category and category.lower().strip() == category_lower:
                final_score += 0.15  # tune as needed

            # ✅ Tone / style boost (funny, premium, cinematic, etc.)
            if tones_lower:
                tone_matches = tones_lower.intersection(tags_lower)
                if tone_matches:
                    final_score += 0.05 * len(tone_matches)

            # ✅ Region boost (e.g., "punjab" tag)
            if region_lower and region_lower in tags_lower:
                final_score += 0.1

            re_ranked.append(
                RetrievedExample(
                    id=str(res.id),
                    title=res.title or "",
                    content=res.content or "",
                    category=category,
                    tags=res.tags or [],
                    score=final_score,
                )
            )

        # 🔹 Step 3: Sort by final score descending and trim
        re_ranked.sort(key=lambda x: x.score, reverse=True)
        final = re_ranked[: preferences.max_examples]

        logger.info(
            "✅ [RETRIEVAL] Returning %d curated examples (from %d base results)",
            len(final),
            len(base_results),
        )

        return final


# Singleton-style instance to import elsewhere
example_retrieval_service = ExampleRetrievalService()
