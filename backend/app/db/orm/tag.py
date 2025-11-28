from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Tag(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)

    examples = relationship("PromptExample", secondary="example_tags", back_populates="tags")
