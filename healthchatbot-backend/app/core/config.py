from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from decouple import config


class Settings:
    """Centralised configuration for the assistant."""

    def __init__(self):
        # Azure OpenAI
        self.azure_endpoint: str = config("AZURE_OPENAI_ENDPOINT", default="")
        self.azure_api_key: str = config("AZURE_OPENAI_API_KEY", default="")
        self.azure_deployment: str = config("AZURE_OPENAI_DEPLOYMENT", default="")
        self.azure_embedding_deployment: str = config(
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", default=""
        )

        # Performance / reliability
        self.llm_timeout_seconds: float = config(
            "LLM_TIMEOUT_SECONDS", cast=float, default=6.0
        )
        self.retry_attempts: int = 3
        self.cache_ttl_seconds: int = config(
            "CACHE_TTL_SECONDS", cast=int, default=600
        )

        # Retrieval settings
        self.chroma_persist_dir: Path = Path(
            config("CHROMA_PERSIST_DIR", default=".chroma")
        )
        self.chroma_top_k: int = config("CHROMA_TOP_K", cast=int, default=3)

        # UI / prompt behaviour
        self.max_history: int = config("MAX_HISTORY_MESSAGES", cast=int, default=3)
        self.fallback_response: str = (
            "I could not reach the medical knowledge service right now. "
            "For urgent concerns call local emergency services (108) or consult a clinician."
        )

        # Ensure telemetry is disabled globally for Chroma
        os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
        os.environ.setdefault("CHROMA_TELEMETRY", "False")


settings = Settings()
