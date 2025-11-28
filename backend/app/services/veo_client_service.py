# app/services/veo_client.py

import os
import time
from typing import Optional

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class VeoClient:
    """
    Wrapper around Google GenAI SDK to handle:
    - Generating still images (Gemini 2.5 Flash Image)
    - Starting Veo3 long-running video operations
    - Polling operations
    - Downloading the final video

    Clean + reusable across agents & pipeline.
    """

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("Missing GOOGLE_API_KEY in environment.")

        self.client = genai.Client(api_key=api_key)

    # ---------------------------------------------------------
    # Singleton-style helpers (optional)
    # ---------------------------------------------------------
    _instance = None

    @classmethod
    def get_instance(cls) -> "VeoClient":
        if cls._instance is None:
            cls._instance = VeoClient()
        return cls._instance

    # ---------------------------------------------------------
    # Step 1 — Generate image for video prompt
    # ---------------------------------------------------------
    def generate_image(self, prompt: str):
        """
        Generates a still image using Gemini Flash Image.
        """

        result = self.client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config={"response_modalities": ['IMAGE']}
        )

        return result

    # ---------------------------------------------------------
    # Step 2 — Start Veo3 long-running operation
    # ---------------------------------------------------------
    def start_video_generation(self, prompt: str, image_part: Optional[types.Part] = None):
        """
        Begins Veo3 video generation.
        Returns an operation object (long-running).
        """

        if image_part:
            operation = self.client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt,
                image=image_part.as_image()
            )
        else:
            operation = self.client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt
            )

        return operation

    # ---------------------------------------------------------
    # Step 3 — Poll operation (used by /pipeline/poll)
    # ---------------------------------------------------------
    def poll_operation(self, operation_id: str):
        """
        Returns the latest status of a long-running Veo3 operation.
        """

        operation = self.client.operations.get(operation_id)
        return operation

    # ---------------------------------------------------------
    # Utility — OPTIONAL blocking poll (not used in API)
    # ---------------------------------------------------------
    def wait_until_done(self, operation, poll_seconds: int = 10):
        """
        Blocking polling loop — NOT used by API.
        Provided only for CLI / testing convenience.
        """

        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(poll_seconds)
            operation = self.client.operations.get(operation)

        return operation

    # ---------------------------------------------------------
    # Step 4 — Download final video
    # ---------------------------------------------------------
    def download_video(self, video_obj, output_path: str):
        """
        Downloads a Veo-generated video to a file.
        """

        self.client.files.download(file=video_obj.video)
        video_obj.video.save(output_path)
        return output_path
