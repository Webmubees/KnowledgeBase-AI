from fastapi import FastAPI
from pydantic import BaseModel

from .rag import answer_question


app = FastAPI(
    title="KnowledgeBase AI",
    description="Local RAG-based knowledge assistant",
    version="1.0.0"
)


# --------------------------------
# Request model
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

@app.get("/")
def root():

    return {
        "name": "KnowledgeBase AI",
        "version": "1.0.0",
        "description": "Local RAG-based knowledge assistant",
        "status": "running",
        "docs": "/docs"
    }


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
def chat(
    request: ChatRequest
):

    answer, results = answer_question(
        request.question
    )


    # -----------------------------
    # No relevant information
    # -----------------------------

    if results is None:

        return {
            "question": request.question,
            "answer": answer,
            "sources": []
        }


    # -----------------------------
    # Extract metadata
    # -----------------------------

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    sources = []


    for metadata, distance in zip(
        metadatas,
        distances
    ):

        sources.append(
            {
                "source": metadata.get(
                    "source",
                    "unknown"
                ),

                "chunk": metadata.get(
                    "chunk",
                    -1
                ),

                "page": metadata.get("page"),

                "document_type": metadata.get(
                    "document_type",
                    "unknown"
                ),

                "distance": float(
                    distance
                )
            }
        )


    # -----------------------------
    # Return structured response
    # -----------------------------

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }