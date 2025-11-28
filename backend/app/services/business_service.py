# app/services/business_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.orm.business import Business
from app.schemas.business_schema import BusinessProfile
import logging

logger = logging.getLogger("backend")


class BusinessService:

    async def create_business(
        self,
        db: AsyncSession,
        business_data: BusinessProfile
    ) -> int:
        """
        Create a new Business entry in PostgreSQL.
        Returns the newly created business ID.
        """

        db_obj = Business(
            name=business_data.business_name,
            website_url=business_data.website,
            raw_input=business_data.raw_input,
            enriched_profile=business_data.model_dump(),
            category=None,  # Will be filled by Example Retrieval Agent
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        logger.info(f"🟢 Business created in DB with ID={db_obj.id}")
        return db_obj.id

    async def get_business(self, db: AsyncSession, business_id: int) -> Business | None:
        """
        Fetch a business entry by ID.
        """
        result = await db.execute(
            select(Business).where(Business.id == business_id)
        )
        return result.scalar_one_or_none()

    async def update_business_category(
        self, db: AsyncSession, business_id: int, category: str
    ) -> None:
        """
        Update the category chosen by Example Retrieval / Classification Agent.
        """

        await db.execute(
            update(Business)
            .where(Business.id == business_id)
            .values(category=category)
        )
        await db.commit()

        logger.info(f"📦 Business {business_id} category updated → {category}")

    async def list_all_businesses(self, db: AsyncSession):
        """
        Fetch all businesses — helpful for admin tools.
        """
        result = await db.execute(select(Business))
        return result.scalars().all()


# Export singleton
business_service = BusinessService()
