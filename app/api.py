from fastapi import FastAPI
from pydantic import BaseModel

from rag import answer_question


app = FastAPI(
    title="KnowledgeBase AI",
    description="Local RAG-based knowledge assistant",
    version="1.0.0"
)


class QuestionRequest(BaseModel):

    question: str


class QuestionResponse(BaseModel):

    answer: str


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/chat", response_model=QuestionResponse)
def chat(request: QuestionRequest):

    answer, _ = answer_question(
        request.question
    )

    return {
        "answer": answer
    }