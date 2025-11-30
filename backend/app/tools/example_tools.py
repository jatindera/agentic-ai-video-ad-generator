# app/tools/example_tools.py

import asyncio
from typing import List, Dict
from google.adk.tools.tool_context import ToolContext

from app.db.database import async_session
from app.db.orm.prompt_example import PromptExample
from sqlalchemy import select
from sqlalchemy.orm import selectinload
# Observability
from app.observability import configure_logging, get_logger

# Configure logging once
configure_logging()
logger = get_logger(__name__)


async def fetch_examples_by_ids(ids: List[str]) -> Dict:
    """Retrieve full creative examples from PostgreSQL using a list of IDs.

    Args:
        ids (List[str]):
            A list of example IDs to fetch from the database.
            These IDs typically come from `search_similar_examples`.

    Returns:
        Dict:
            A dictionary with this exact structure:

            {
                "examples": [
                    {
                        "id": "...",
                        "title": "...",
                        "prompt_text": "...",
                        "prompt_json": {...},
                        "business_type": "...",
                        "ad_style": "...",
                        "tone": "...",
                        "target_audience": "...",
                        "tags": [...],
                    },
                    ...
                ],
                "error": None or "error_message"
            }

   
    """

    logger.info(f"XXXXXXXXXX fetch_examples_by_ids called XXXXXXXXXX -> {ids}")

    # ----------------------------------------------------------------------
    # 0. Validate input — empty list means no fetch should occur.
    # ----------------------------------------------------------------------
    if not ids:
        return {"examples": [], "error": None}


    try:
        # ----------------------------------------------------------------------
        # 1. Create an async DB session.
        #    Load examples + tags with eager relationship loading.
        # ----------------------------------------------------------------------
        async with async_session() as session:
            stmt = (
                select(PromptExample)
                .where(PromptExample.id.in_(ids))
                .options(selectinload(PromptExample.tags))  # load tags in one query
            )

            result = await session.execute(stmt)
            rows = result.scalars().all()

        # ----------------------------------------------------------------------
        # 2. Format database rows into simple JSON objects.
        #    This ensures LLM agents receive clean, predictable output.
        # ----------------------------------------------------------------------
        formatted = []

        for row in rows:
            formatted.append({
                "id": row.id,
                "title": row.title,
                "prompt_text": row.prompt_text,
                "prompt_json": row.prompt_json,
                "business_type": row.business_type,
                "ad_style": row.ad_style,
                "tone": row.tone,
                "target_audience": row.target_audience,
                "tags": [t.name for t in row.tags],  # flatten tag names
            })

        # ----------------------------------------------------------------------
        # 3. Return results to the agent exactly in this format.
        # ----------------------------------------------------------------------
        return {
            "examples": formatted,
            "error": None
        }

    except Exception as e:
        # ----------------------------------------------------------------------
        # 4. Fail gracefully — never break LLM workflows.
        # ----------------------------------------------------------------------
        return {
            "examples": [],
            "error": str(e)
        }
