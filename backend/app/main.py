from fastapi import FastAPI, HTTPException

from backend.app.config import settings
from backend.app.schemas import ChatRequest, ChatResponse
from backend.app.services.rag_pipeline import rag_pipeline
from fastapi import UploadFile, File
from backend.app.services.document_service import document_service
from backend.app.services.document_manager import document_manager
from backend.app.services.knowledge_gap_tracker import knowledge_gap_tracker
from backend.app.services.knowledge_gap_analyzer import knowledge_gap_analyzer
from backend.app.services.learning_recommender import learning_recommender
from backend.app.services.dashboard_service import dashboard_service


app = FastAPI(
    title="ExpertMind API",
    description="AI Knowledge Mentor powered by RAG and Ollama.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to ExpertMind API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "llm_model": settings.LLM_MODEL
    }


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        result = rag_pipeline.ask(
            question=request.question,
            session_id=request.session_id
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your question."
        )

@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    try:
        result = await document_service.upload_and_process(file)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Document processing failed."
        )

@app.get("/api/v1/documents")
def list_documents():

    try:
        documents = document_manager.list_documents()

        return {
            "total_documents": len(documents),
            "documents": documents
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve documents."
        )


@app.delete("/api/v1/documents/{document_id}")
def delete_document(document_id: str):
    try:
        return document_manager.delete_document(document_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@app.get("/api/v1/knowledge-gaps")
def get_knowledge_gaps(session_id: str | None = None):

    try:
        gaps = knowledge_gap_tracker.get_gaps(
            session_id=session_id
        )

        return {
            "total_gaps": len(gaps),
            "knowledge_gaps": gaps
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve knowledge gaps."
        )


@app.delete("/api/v1/knowledge-gaps")
def clear_knowledge_gaps(session_id: str | None = None):

    try:
        deleted_count = knowledge_gap_tracker.clear_gaps(
            session_id=session_id
        )

        return {
            "message": "Knowledge gaps cleared successfully.",
            "deleted_count": deleted_count
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not clear knowledge gaps."
        )

@app.get("/api/v1/knowledge-gaps/analyze")
def analyze_knowledge_gaps(session_id: str | None = None):

    try:
        result = knowledge_gap_analyzer.analyze(
            session_id=session_id
        )

        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not analyze knowledge gaps."
        )

@app.get("/api/v1/learning-recommendations")
def get_learning_recommendations(session_id: str | None = None):

    return learning_recommender.generate_recommendations(
        session_id=session_id
    )

@app.get("/api/v1/dashboard")
def get_dashboard(session_id: str | None = None):

    try:
        return dashboard_service.get_dashboard(
            session_id=session_id
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve dashboard data."
        )