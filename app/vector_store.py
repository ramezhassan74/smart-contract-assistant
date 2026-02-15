"""
Smart Contract Assistant - Vector Store (FAISS)
"""

from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config import VECTOR_STORE_DIR
from app.embeddings import get_embeddings


def create_vector_store(documents: list[Document]) -> FAISS:
    """Create a new FAISS vector store from a list of documents and save it."""
    if not documents:
        raise ValueError("No documents provided to create vector store.")

    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)

    # Save to disk
    Path(VECTOR_STORE_DIR).mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(VECTOR_STORE_DIR))

    print(f"✅ Vector store created with {len(documents)} chunks → {VECTOR_STORE_DIR}")
    return vector_store


def load_vector_store() -> FAISS:
    """Load an existing FAISS vector store from disk."""
    if not Path(VECTOR_STORE_DIR).exists():
        raise FileNotFoundError(
            f"Vector store not found at {VECTOR_STORE_DIR}. "
            "Please run ingestion first."
        )

    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print(f"✅ Vector store loaded from {VECTOR_STORE_DIR}")
    return vector_store
