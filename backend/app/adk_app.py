from google.adk.apps import App
from google.adk.apps.app import ResumabilityConfig
from app.video_pipeline_app.root_agent import root_agent # very important, makes sure you use object
from app.core.config import settings

APP_NAME = settings.app_name

video_app = App(
    name=APP_NAME,
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
