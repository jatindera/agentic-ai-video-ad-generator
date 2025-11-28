# app/services/example_service.py

import logging
import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.orm.prompt_example import PromptExample
from app.db.orm.tag import Tag
from app.db.orm.example_tag import ExampleTag

from app.services.embedding_service import embedding_service
from app.services.pinecone_service import pinecone_service

from app.schemas.example_schema import ExampleSearchResult


logger = logging.getLogger("backend")


class ExampleService:

    # ------------------------------------------------------------
    # CREATE EXAMPLE (DB + Pinecone)
    # ------------------------------------------------------------
    async def create_example(
        self,
        db: AsyncSession,
        title: str,
        prompt_text: Optional[str],
        prompt_json: Optional[dict],
        business_type: Optional[str],
        ad_style: Optional[str],
        tone: Optional[str],
        target_audience: Optional[str],
        tags: List[str],
    ):

        example_id = str(uuid.uuid4())

        # -------------------------------------------------------------------
        # (1) Store example in PostgreSQL
        # -------------------------------------------------------------------
        db_example = PromptExample(
            id=example_id,
            title=title,
            prompt_text=prompt_text,
            prompt_json=prompt_json,
            business_type=business_type,
            ad_style=ad_style,
            tone=tone,
            target_audience=target_audience,
        )

        db.add(db_example)

        # -------------------------------------------------------------------
        # (2) Store tags
        # -------------------------------------------------------------------
        tag_ids = []
        for tag_name in tags:
            clean = tag_name.lower().strip()
            result = await db.execute(select(Tag).where(Tag.name == clean))
            tag_obj = result.scalars().first()

            if not tag_obj:
                tag_obj = Tag(name=clean)
                db.add(tag_obj)

            await db.flush()
            tag_ids.append(tag_obj.id)

        # insert example → tags relationship
        for tag_id in tag_ids:
            db.add(ExampleTag(example_id=example_id, tag_id=tag_id))

        await db.commit()

        # -------------------------------------------------------------------
        # (3) Generate Embedding (text OR JSON)
        # -------------------------------------------------------------------
        embedding_input = (
            prompt_text
            if prompt_text
            else (str(prompt_json) if prompt_json else "")
        )


        embedding = await embedding_service.get_embedding(embedding_input)

        # -------------------------------------------------------------------
        # (4) Upsert into Pinecone
        # -------------------------------------------------------------------
        metadata = {
            "id": example_id,
            "title": title,
            "business_type": business_type or "",
            "ad_style": ad_style or "",
            "tone": tone or "",
            "target_audience": target_audience or "",
            "tags": tags,                    # OK: list of strings
            "has_json": bool(prompt_json),   # boolean is allowed
        }



        await pinecone_service.upsert_example(
            example_id=example_id,
            embedding=embedding,
            metadata=metadata,
        )

        return example_id

    # ------------------------------------------------------------
    # 🔍 SEARCH EXAMPLES (semantic + metadata filters)
    # ------------------------------------------------------------
    async def search_examples(
        self,
        db: AsyncSession,
        query: str,
        business_type: Optional[str],
        ad_style: Optional[str],
        tone: Optional[str],
        target_audience: Optional[str],
        tags: Optional[List[str]],
        top_k: int = 5,
    ) -> List[ExampleSearchResult]:

        logger.info("🔍 Embedding search query...")
        embedding = await embedding_service.get_embedding(query)

        # Build metadata filter for Pinecone
        pinecone_filter = {}

        if business_type:
            pinecone_filter["business_type"] = business_type
        if ad_style:
            pinecone_filter["ad_style"] = ad_style
        if tone:
            pinecone_filter["tone"] = tone
        if target_audience:
            pinecone_filter["target_audience"] = target_audience
        if tags:
            pinecone_filter["tags"] = {"$in": tags}

        # 🔍 Query Pinecone
        matches = await pinecone_service.query_examples(
            embedding=embedding,
            top_k=top_k,
            metadata_filter=pinecone_filter,
        )

        if not matches:
            return []

        example_ids = [m.id for m in matches]
        if not example_ids:
            return []

        # Load DB objects
        stmt = (
            select(PromptExample)
            .where(PromptExample.id.in_(example_ids))
            .options(selectinload(PromptExample.tags))
        )
        result = await db.execute(stmt)
        examples = result.scalars().all()

        db_by_id = {ex.id: ex for ex in examples}

        # Merge DB + Pinecone
        final_results: List[ExampleSearchResult] = []
        for match in matches:
            ex = db_by_id.get(match.id)
            if not ex:
                continue

            tag_names = [t.name for t in ex.tags]

            final_results.append(
                ExampleSearchResult(
                    id=ex.id,
                    title=ex.title,
                    prompt_text=ex.prompt_text,
                    prompt_json=ex.prompt_json,
                    business_type=ex.business_type,
                    ad_style=ex.ad_style,
                    tone=ex.tone,
                    target_audience=ex.target_audience,
                    tags=tag_names,
                    score=float(match.score or 0.0),
                )
            )

        return final_results


example_service = ExampleService()
