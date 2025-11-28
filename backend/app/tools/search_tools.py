# app/tools/search_tools.py

import os
import asyncio
from typing import Dict, List
from dotenv import load_dotenv
from pinecone import Pinecone

from app.services.embedding_service import embedding_service

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# -----------------------------------------------------
# 🔧 Initialize Pinecone Client
# -----------------------------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

try:
    index = pc.Index(PINECONE_INDEX)
except Exception:
    index = None


async def search_similar_examples(query: str, top_k: int = 5) -> Dict:
    """
Return at most 2 example IDs from Pinecone with similarity >= 0.9.
If none meet the threshold, return an empty list.
    """

    print("🔍 search_similar_examples (with ≥0.9 score filtering + max 2 results) called")

    # -----------------------------
    # Validate Pinecone index
    # -----------------------------
    if index is None:
        return {
            "ids": [],
            "error": f"Pinecone index '{PINECONE_INDEX}' not available"
        }

    try:
        # 1. Generate embedding
        embedding: List[float] = await embedding_service.get_embedding(query)

        # 2. Perform Pinecone vector search
        response = await asyncio.to_thread(
            index.query,
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
        )

        if not response.matches:
            return {"ids": [], "error": None}

        # 3. Filter matches by score >= 0.9
        qualified = []
        for match in response.matches:
            raw_score = match.score

            # Normalize score to 0–1 scale if needed
            score = raw_score / 100 if raw_score > 1 else raw_score
            print("=========Score is============")
            print(score)
            print("=============================")

            if score >= 0.9:
                md = match.metadata or {}
                example_id = md.get("id", match.id)
                if example_id:
                    qualified.append((example_id, score))

        # No matches above threshold
        if not qualified:
            return {"ids": [], "error": None}

        # 4. Sort by highest score
        qualified.sort(key=lambda x: x[1], reverse=True)

        # 5. Keep ONLY top 2 IDs
        final_ids = [item[0] for item in qualified[:2]]

        return {
            "ids": final_ids,
            "error": None
        }

    except Exception as e:
        return {
            "ids": [],
            "error": str(e)
        }
