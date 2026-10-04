import os

from dotenv import load_dotenv


load_dotenv()

MODEL_NAME = "google_genai:gemini-3.5-flash-lite"

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError(
        "Defina GOOGLE_API_KEY no arquivo .env antes de iniciar a API."
    )
