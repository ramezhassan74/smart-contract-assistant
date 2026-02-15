from langchain_google_genai import GoogleGenerativeAIEmbeddings
from google import genai
from app.config import GOOGLE_API_KEY

# Possible embedding model names to try (in order of preference)
EMBEDDING_MODELS = [
    "models/gemini-embedding-001",
    "models/text-embedding-004",
    "models/embedding-001",
    "text-embedding-004",
    "embedding-001",
]


def _find_embedding_model() -> str:
    """Auto-detect an available embedding model from Google's API."""
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        models = client.models.list()
        for model in models:
            name = model.name
            if "embed" in name.lower():
                print(f"✅ Found embedding model: {name}")
                return name
    except Exception as e:
        print(f"⚠️ Could not list models: {e}")

    # Return the most likely working model
    return "models/gemini-embedding-001"


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY is not set. "
            "Please set it in a .env file or as an environment variable."
        )

    model_name = _find_embedding_model()

    return GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=GOOGLE_API_KEY,
    )
