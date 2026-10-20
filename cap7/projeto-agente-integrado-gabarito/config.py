import os

from dotenv import load_dotenv


load_dotenv()

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "google_genai:gemini-3.6-flash",
)
CATALOGO_API_URL = os.getenv(
    "CATALOGO_API_URL",
    "http://127.0.0.1:8001",
).rstrip("/")


def validar_configuracao() -> None:
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "Defina GOOGLE_API_KEY no arquivo .env antes de iniciar a aplicação."
        )
