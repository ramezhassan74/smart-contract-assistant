from app.config import RETRIEVER_K
from app.vector_store import load_vector_store


def get_retriever():
    """Create a retriever from the vector store."""
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVER_K},
    )
    return retriever
