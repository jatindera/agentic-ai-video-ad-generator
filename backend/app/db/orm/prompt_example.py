# app/db/orm/prompt_example.py

from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class PromptExample(Base):
    __tablename__ = "prompt_examples"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)

    # text prompt OR json prompt
    prompt_text = Column(Text, nullable=True)
    prompt_json = Column(JSON, nullable=True)

    # optional structured fields
    business_type = Column(String(100), nullable=True)
    ad_style = Column(String(100), nullable=True)
    tone = Column(String(100), nullable=True)
    target_audience = Column(String(255), nullable=True)

    # Tags relationship
    tags = relationship("Tag", secondary="example_tags", back_populates="examples")
