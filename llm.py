import os

from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT

MODEL_NAME = "gemini-flash-latest"


def get_api_key():
    """Read the Gemini API key from the environment, returning None if it is missing."""
    return os.getenv("GEMINI_API_KEY")


def build_client():
    """Create and return a Gemini API client authenticated with the API key from the environment."""
    return genai.Client(api_key=get_api_key())


def generate_json(client, prompt):
    """Send a prompt to Gemini under the PantryChef system prompt and return the raw JSON response text."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    return response.text
