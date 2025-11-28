# app/api/examples/test_retrieval_routes.py (optional, dev-only)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.services.retrieval_service import (
    example_retrieval_service,
    RetrievalPreferences,
)

router = APIRouter()


@router.post("/test-business-retrieval")
async def test_business_retrieval(
    db: AsyncSession = Depends(get_session),
):
    business_description = "A small futuristic car showroom that sells premium electric vehicles like Tesla."

    prefs = RetrievalPreferences(
        category="automotive",
        tones=["futuristic", "cinematic"],
        region=None,
        max_examples=3,
    )

    results = await example_retrieval_service.get_examples_for_business(
        db=db,
        business_description=business_description,
        preferences=prefs,
    )

    return {"results": [r.model_dump() for r in results]}
