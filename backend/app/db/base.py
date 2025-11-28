# Used in alembic env.py
#
# Alembic needs to know:
# 1. Which SQLAlchemy Base class all models inherit from.
# 2. Where to find the collected metadata for generating migrations.
#
# Without this information, Alembic cannot autogenerate migrations.


from sqlalchemy.orm import DeclarativeBase

# This Base will be used by all ORM models
class Base(DeclarativeBase):
    pass
