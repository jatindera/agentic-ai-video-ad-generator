# backend/app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import engine
from app.db.base import Base

import os
os.environ["GOOGLE_ADK_DISABLE_OTEL"] = "true"
os.environ["OTEL_PYTHON_DISABLED"] = "true"



# Routers
from app.api.agents.routes import router as agents_router
from app.api.examples.routes import router as examples_router

# ADK Web Implementation (Only in developement mode)
from google.adk.cli.fast_api import get_fast_api_app

# Observability
from app.observability import configure_logging, get_logger

# Configure logging once
configure_logging()
logger = get_logger(__name__)

# Working directory = backend/
WORKING_DIR = os.getcwd()

# Path to agents folder
AGENT_DIR = os.path.join(WORKING_DIR, "app", settings.app_name)

print("AGENT_DIR =", AGENT_DIR)

SESSION_DB_URL = settings.adk_session_postgres_url


@asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    logger.info("FastAPI backend started successfully")
    logger.info(f"Environment: {settings.app_env}")

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

    yield

    logger.info("FastAPI backend shutdown")

##################################################
####        use Following for ADK WEB         ####
##################################################
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=["*"],
    lifespan=lifespan_wrapper,
    web=True,
    a2a=True,
    reload_agents=True,
    extra_plugins=[
        "app.observability.plugins.adk_observability_plugin.ADKObservabilityPlugin"
    ]
)


# Main FastAPI app
# app = FastAPI(
#     title=settings.app_name,
#     lifespan=lifespan_wrapper
# )

 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#################################################################
##### Session and Runner implementation in following router #####
#################################################################
app.include_router(agents_router, prefix="/agents", tags=["Agents"])

# For vector search
app.include_router(examples_router, prefix="/examples", tags=["Examples"])

# health test
@app.get("/health")
def health():
    logger.info("Health endpoint hit!")
    return {
        "status": "ok", 
        "env": settings.app_env
        }
