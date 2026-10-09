
from pathlib import Path

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from .rag import answer_question
from .index import main as index_documents
from .document_registry import (
    load_registry,
    get_file_status,
    save_registry,
    remove_from_registry
)

from .vector_store import (
    delete_document as delete_document_vectors
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# --------------------------------
# Application configuration
# --------------------------------

app = FastAPI(
    title="KnowledgeBase AI",
    description="Local RAG-based knowledge assistant",
    version="1.0.0"
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)

DOCUMENTS_DIR = Path("data/documents")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# --------------------------------
# Request models
# --------------------------------

class ChatRequest(BaseModel):
    question: str


# --------------------------------
# Response models
# --------------------------------

class Source(BaseModel):
    source: str
    chunk: int
    page: int | None = None
    document_type: str
    distance: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]


# --------------------------------
# Root endpoint
# --------------------------------

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(FRONTEND_DIR / "index.html")

# --------------------------------
# Health endpoint
# --------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------
# Chat endpoint
# --------------------------------

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    answer, results = answer_question(
        request.question
    )

    # No relevant information was found.
    if results is None:
        return {
            "question": request.question,
            "answer": answer,
            "sources": []
        }

    # Extract metadata and distances from ChromaDB.
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    sources = []

    for metadata, distance in zip(metadatas, distances):
        sources.append({
            "source": metadata.get("source", "unknown"),
            "chunk": metadata.get("chunk", -1),
            "page": metadata.get("page"),
            "document_type": metadata.get(
                "document_type", "unknown"
            ),
            "distance": float(distance)
        })

    # Return the answer and source citations.
    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }


# --------------------------------
# Document upload endpoint
# --------------------------------

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    filename = Path(file.filename or "").name

    if not filename or filename in {".", ".."}:
        raise HTTPException(
            status_code=400,
            detail="A valid filename is required."
        )

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are supported."
        )

    DOCUMENTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = DOCUMENTS_DIR / filename

    if destination.exists():
        raise HTTPException(
            status_code=409,
            detail="A document with this filename already exists."
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB."
        )

    try:
        # Create the file without overwriting an existing file.
        with destination.open("xb") as output_file:
            output_file.write(content)

        # Run the existing indexing pipeline.
        await run_in_threadpool(index_documents)

        return {
            "filename": filename,
            "status": "indexed",
            "message": "Document uploaded and indexing completed."
        }

    except HTTPException:
        destination.unlink(missing_ok=True)
        raise

    except Exception as exc:
        # Remove the uploaded file if indexing fails.
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Indexing failed. Check the application logs."
        ) from exc

    finally:
        await file.close()


# --------------------------------
# List documents endpoint
# --------------------------------

@app.get("/documents")
def list_documents():

    registry = load_registry()
    documents = []

    if DOCUMENTS_DIR.exists():

        for file_path in sorted(DOCUMENTS_DIR.iterdir()):

            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
                continue

            file_status = get_file_status(
                file_path,
                registry
            )

            if file_status == "unchanged":
                status = "indexed"

            elif file_status == "modified":
                status = "modified"

            else:
                status = "not_indexed"

            documents.append({
                "filename": file_path.name,
                "file_type": file_path.suffix.lower().lstrip("."),
                "status": status
            })

    return {
        "documents": documents,
        "total": len(documents)
    }



# --------------------------------
# Delete document endpoint
# --------------------------------

@app.delete("/documents/{filename}")
def delete_uploaded_document(filename: str):

    # Validate the filename to prevent path traversal.
    if (
        not filename
        or filename in {".", ".."}
        or "/" in filename
        or "\\" in filename
        or Path(filename).name != filename
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT documents are supported."
        )

    destination = DOCUMENTS_DIR / filename

    registry = load_registry()

    # Check whether the file or registry entry exists.
    if not destination.is_file() and filename not in registry:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:
        # 1. Delete all ChromaDB vectors for this document.
        delete_document_vectors(filename)

        # 2. Remove the document from the registry.
        remove_from_registry(filename, registry)
        save_registry(registry)

        # 3. Delete the original file if it exists.
        if destination.is_file():
            destination.unlink()

        return {
            "filename": filename,
            "status": "deleted",
            "message": (
                "Document, vectors, and registry entry "
                "removed successfully."
            )
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document deletion failed. Check application logs."
        ) from exc
