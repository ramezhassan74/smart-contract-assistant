from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from app.vector_store import create_vector_store


LOADER_MAP = {
    "*.pdf": PyPDFLoader,
    "*.txt": TextLoader,
    "*.md": TextLoader,
    "*.sol": TextLoader,
}


def load_documents() -> list[Document]:
    """Load all supported documents from the docs directory."""
    docs_path = Path(DOCS_DIR)
    if not docs_path.exists():
        raise FileNotFoundError(f"Documents directory not found: {DOCS_DIR}")

    all_docs: list[Document] = []

    for glob_pattern, loader_cls in LOADER_MAP.items():
        try:
            loader = DirectoryLoader(
                str(docs_path),
                glob=glob_pattern,
                loader_cls=loader_cls,
                show_progress=True,
                use_multithreading=True,
            )
            docs = loader.load()
            if docs:
                print(f"  📄 Loaded {len(docs)} pages from {glob_pattern} files")
                all_docs.extend(docs)
        except Exception as e:
            print(f"  ⚠️ Warning loading {glob_pattern}: {e}")

    if not all_docs:
        raise ValueError(
            f"No documents found in {DOCS_DIR}. "
            "Please add .pdf, .txt, .md, or .sol files."
        )

    print(f"📚 Total documents loaded: {len(all_docs)}")
    return all_docs


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def ingest() -> int:
    """
    Full ingestion pipeline: load → split → embed → store.
    Returns the number of chunks stored.
    """
    print("🚀 Starting ingestion pipeline...")
    print("=" * 50)

    documents = load_documents()

    chunks = split_documents(documents)
    create_vector_store(chunks)

    print("=" * 50)
    print(f"🎉 Ingestion complete! {len(chunks)} chunks stored.")
    return len(chunks)
