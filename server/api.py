from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import shutil

from app.config import DOCS_DIR
from app.ingestion import ingest
from app.qa_chain import ask


app = FastAPI(
    title="Smart Contract Assistant API",
    description="RAG-based Q&A API for Smart Contracts & Solidity",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[dict]


class IngestResponse(BaseModel):
    message: str
    chunks_count: int


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Smart Contract Assistant"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result = ask(request.question)
        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Vector store not found. Please run /ingest first.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", response_model=IngestResponse)
def run_ingestion():
    try:
        chunks_count = ingest()
        return IngestResponse(
            message="Ingestion completed successfully!",
            chunks_count=chunks_count,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".txt", ".md", ".sol"}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_ext}'. "
                   f"Allowed: {', '.join(allowed_extensions)}",
        )

    docs_path = Path(DOCS_DIR)
    docs_path.mkdir(parents=True, exist_ok=True)

    dest = docs_path / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"message": f"File '{file.filename}' uploaded successfully.", "path": str(dest)}
