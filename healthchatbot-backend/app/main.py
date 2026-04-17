from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.session_manager import session_manager
from app.services.pipeline import assistant_orchestrator
from app.routes import whatsapp

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Swasthya Setu API",
    description="Multilingual healthcare assistant with resilient pipeline",
    version="3.0.0",
)

static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.include_router(whatsapp.router)


class HistoryTurn(BaseModel):
    role: str = Field(default="user")
    content: str


class HealthQuery(BaseModel):
    message: str
    language: Optional[str] = None
    user_id: Optional[str] = "web"
    history: Optional[List[HistoryTurn]] = None


class HealthResponse(BaseModel):
    response: str
    intent: str
    severity: str
    emergency: bool
    cached: bool = False
    meta: dict = Field(default_factory=dict)


@app.get("/")
async def index():
    if static_dir.exists():
        return FileResponse(static_dir / "index.html")
    return {"status": "ok", "message": "Swasthya Setu backend"}


@app.get("/health")
async def health_check():
    stats = session_manager.get_stats()
    return {
        "status": "healthy",
        "sessions": stats,
        "cache_ttl": settings.cache_ttl_seconds,
        "llm_configured": bool(settings.azure_api_key and settings.azure_endpoint),
    }


@app.post("/api/query", response_model=HealthResponse)
async def api_query(query: HealthQuery):
    result = await assistant_orchestrator.handle_query(
        message=query.message,
        user_id=query.user_id or "web",
        language=query.language,
        history=[turn.model_dump() for turn in query.history or []],
    )
    return result


@app.post("/api/retry", response_model=HealthResponse)
async def api_retry(query: HealthQuery):
    """Explicit retry endpoint in case the client wants to bypass cache."""
    return await assistant_orchestrator.handle_query(
        message=query.message,
        user_id=query.user_id or "web",
        language=query.language,
        history=[turn.model_dump() for turn in query.history or []],
    )
