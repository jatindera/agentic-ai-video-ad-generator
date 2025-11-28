from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base

class ExampleTag(Base):
    __tablename__ = "example_tags"

    example_id = Column(String, ForeignKey("prompt_examples.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)
