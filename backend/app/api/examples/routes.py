# app/api/examples/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.services.example_service import example_service

from app.schemas.example_schema import (
    ExampleCreateRequest,
    ExampleSearchRequest,
    ExampleSearchResponse,
)


router = APIRouter()


# -------------------------------------------------------------
# POST /examples/upload
# Create + store example prompt (text or JSON) + embed + Pinecone
# -------------------------------------------------------------
@router.post("/upload")
async def upload_example(
    example_data: ExampleCreateRequest,
    db: AsyncSession = Depends(get_session),
):
    """
    Upload a new example for the creative pipeline:
    - Supports raw text prompts OR structured JSON prompts
    - Stores metadata in PostgreSQL
    - Generates embeddings (based on text or JSON)
    - Stores embedding + metadata in Pinecone
    """

    try:
        example_id = await example_service.create_example(
            db=db,
            title=example_data.title,
            prompt_text=example_data.prompt_text,
            prompt_json=example_data.prompt_json,
            business_type=example_data.business_type,
            ad_style=example_data.ad_style,
            tone=example_data.tone,
            target_audience=example_data.target_audience,
            tags=example_data.tags,
        )

        return {
            "status": "success",
            "example_id": example_id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -------------------------------------------------------------
# POST /examples/search
# Hybrid semantic + metadata filtered vector search
# -------------------------------------------------------------
@router.post("/search", response_model=ExampleSearchResponse)
async def search_examples(
    search_req: ExampleSearchRequest,
    db: AsyncSession = Depends(get_session),
):
    """
    Search stored examples using:
    - semantic similarity via embeddings
    - structured metadata filters:
        * business_type
        * ad_style
        * tone
        * target_audience
        * tags
    """

    try:
        results = await example_service.search_examples(
            db=db,
            query=search_req.query,
            business_type=search_req.business_type,
            ad_style=search_req.ad_style,
            tone=search_req.tone,
            target_audience=search_req.target_audience,
            tags=search_req.tags,
            top_k=search_req.top_k,
        )

        return ExampleSearchResponse(results=results)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
