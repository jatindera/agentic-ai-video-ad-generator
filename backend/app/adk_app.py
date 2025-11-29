from google.adk.apps import App
from google.adk.apps.app import ResumabilityConfig
from app.video_pipeline_app import root_agent
from app.core.config import settings

APP_NAME = settings.app_name

video_app = App(
    name=APP_NAME,
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
