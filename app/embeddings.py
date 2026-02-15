from langchain_google_genai import GoogleGenerativeAIEmbeddings
from google import genai
from app.config import GOOGLE_API_KEY


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

    # Fallback
    return "text-embedding-004"


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
