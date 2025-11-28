from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import setup_logging
import logging

# NEW imports for auto table creation
from app.db.database import engine
from app.db.base import Base

# Routers
from app.api.pipeline.routes import router as pipeline_router
from app.api.agents.routes import router as agents_router
from app.api.examples.routes import router as examples_router
from app.api.examples.test_retrieval_routes import router as test_retrieval_router
from app.api.pipeline.poll_routes import router as poll_router


setup_logging()
logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 FastAPI backend started successfully")
    logger.info(f"Environment: {settings.app_env}")

    # ----------------------------------------------------
    # 📌 Auto-create all database tables on startup
    # ----------------------------------------------------
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("📌 Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")

    yield

    logger.info("🛑 FastAPI backend shutdown")


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pipeline_router, prefix="/pipeline", tags=["Pipeline"])
app.include_router(agents_router, prefix="/agents", tags=["Agents"])
app.include_router(examples_router, prefix="/examples", tags=["Examples"])
app.include_router(test_retrieval_router, prefix="/test-retrieval", tags=["Examples"])
app.include_router(poll_router, prefix="/pipeline", tags=["Pipeline"])


@app.get("/health")
def health():
    logger.info("Health endpoint hit!")
    return {"status": "ok", "env": settings.app_env}
