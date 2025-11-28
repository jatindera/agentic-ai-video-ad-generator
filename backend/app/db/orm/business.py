from sqlalchemy import Column, Integer, String, Text, JSON
from app.db.base import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    website_url = Column(String(500), nullable=True)
    raw_input = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

    user_creative_idea = Column(Text, nullable=True)  # NEW FIELD 🚀

    enriched_profile = Column(JSON, nullable=True)
    category = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Business(name={self.name}, category={self.category})>"
