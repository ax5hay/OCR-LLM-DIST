"""
FastAPI backend wrapper for OCR-LLM-DIST application.
Provides REST API endpoints for the Next.js frontend.
"""

from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import io
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.model_service import run_model, validate_model_parameters
from services.lmstudio_service import (
    check_api_health as lmstudio_health,
    get_available_models as lmstudio_models,
)
from services.ollama_service import (
    check_api_health as ollama_health,
    get_available_models as ollama_models,
)
from utils.file_utils import extract_text_from_doc
from config import ACTIVE_LLM_BACKEND

app = FastAPI(
    title="OCR-LLM API",
    description="REST API for OCR-LLM-DIST with Next.js frontend",
    version="1.0.0",
)

# Add CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation context
conversation_context = {}


@app.get("/api/health")
async def health_check(backend: str = Query("lmstudio", description="Backend to check")):
    """
    Check if the specified backend is healthy.
    
    Args:
        backend: "ollama" or "lmstudio"
    
    Returns:
        JSON with status and backend info
    """
    try:
        if backend == "lmstudio":
            is_healthy = lmstudio_health()
            backend_info = "LMStudio API"
        elif backend == "ollama":
            is_healthy = ollama_health()
            backend_info = "Ollama API"
        else:
            raise HTTPException(status_code=400, detail="Invalid backend")

        if is_healthy:
            return {
                "status": "healthy",
                "backend": backend,
                "message": f"{backend_info} is running",
            }
        else:
            return {
                "status": "unhealthy",
                "backend": backend,
                "message": f"{backend_info} is not responding",
            }
    except Exception as e:
        return {
            "status": "error",
            "backend": backend,
            "message": str(e),
        }


@app.get("/api/models")
async def get_models(backend: str = Query("lmstudio", description="Backend to query")):
    """
    Get available models from the specified backend.
    
    Args:
        backend: "ollama" or "lmstudio"
    
    Returns:
        JSON with list of available models
    """
    try:
        if backend == "lmstudio":
            models = lmstudio_models()
        elif backend == "ollama":
            models = ollama_models()
        else:
            raise HTTPException(status_code=400, detail="Invalid backend")

        return {
            "backend": backend,
            "models": models,
            "count": len(models),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(
    message: str = Query(..., description="User message"),
    model: str = Query(..., description="Model to use"),
    backend: str = Query("lmstudio", description="Backend to use"),
    temperature: float = Query(0.7, ge=0, le=2),
    top_k: int = Query(40, ge=0),
    top_p: float = Query(0.9, ge=0, le=1),
):
    """
    Send a message and get a streaming response.
    
    Args:
        message: User message
        model: Model name
        backend: "ollama" or "lmstudio"
        temperature: Sampling temperature
        top_k: Top-K sampling
        top_p: Nucleus sampling
    
    Returns:
        StreamingResponse with the AI response
    """
    try:
        # Validate parameters
        temp, tk, tp = validate_model_parameters(
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )

        # Add context if available
        full_prompt = message
        if "context" in conversation_context:
            full_prompt = f"Context:\n{conversation_context['context']}\n\nQuestion: {message}"

        # Create generator for streaming
        def generate():
            for chunk in run_model(
                prompt=full_prompt,
                model=model,
                temperature=temp,
                top_k=tk,
                top_p=tp,
                backend=backend,
            ):
                yield chunk.encode("utf-8")

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a document.
    
    Args:
        file: PDF or text file
    
    Returns:
        JSON with extracted content
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Extract text based on file type
        text = ""
        if file.filename.endswith(".pdf"):
            # For PDF files, use fitz
            import fitz
            file_obj = io.BytesIO(contents)
            pdf_doc = fitz.open(stream=file_obj, filetype="pdf")
            for page in pdf_doc:
                text += page.get_text()
            pdf_doc.close()
        elif file.filename.endswith((".txt", ".doc", ".docx")):
            # For text files, decode directly
            try:
                text = contents.decode("utf-8")
            except UnicodeDecodeError:
                text = contents.decode("latin-1")
        else:
            raise HTTPException(
                status_code=400, detail="Unsupported file type. Use PDF or TXT."
            )

        # Store context for future messages
        conversation_context["context"] = text
        conversation_context["filename"] = file.filename

        return {
            "success": True,
            "filename": file.filename,
            "content": text,
            "length": len(text),
            "message": "Document processed successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


@app.get("/api/config")
async def get_config():
    """
    Get current configuration.
    
    Returns:
        JSON with current config
    """
    return {
        "active_backend": ACTIVE_LLM_BACKEND,
        "app_name": "OCR-LLM-DIST",
        "version": "1.0.0",
        "features": [
            "Document Upload",
            "Streaming Chat",
            "Multi-Backend Support",
            "Model Selection",
            "Parameter Tuning",
        ],
    }


@app.post("/api/clear-context")
async def clear_context():
    """
    Clear conversation context.
    
    Returns:
        JSON confirmation
    """
    conversation_context.clear()
    return {
        "success": True,
        "message": "Context cleared",
    }


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "name": "OCR-LLM API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "models": "/api/models",
            "chat": "/api/chat",
            "upload": "/api/upload",
            "config": "/api/config",
            "clear_context": "/api/clear-context",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
