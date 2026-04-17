from __future__ import annotations

import logging
import os
import re
from typing import Any, Dict, List, Tuple

try:
    import chromadb
    from chromadb.config import Settings
except Exception:  # pragma: no cover - fallback when chromadb missing
    chromadb = None
    Settings = None

from app.core.config import settings
from app.services.health_data_loader import HealthDataLoader, health_data

logger = logging.getLogger(__name__)


class RetrievalService:
    """Lightweight retrieval with Chroma + safe fallbacks."""

    def __init__(self, loader: HealthDataLoader):
        self.loader = loader
        self.top_k = settings.chroma_top_k
        self.embedding_cache: Dict[str, List[float]] = {}
        self.client = None
        self.collection = None
        self._bootstrap_chroma()

    def _bootstrap_chroma(self):
        if not chromadb:
            logger.warning("ChromaDB not installed; falling back to in-memory matching.")
            return
        try:
            os.environ.setdefault("CHROMA_TELEMETRY", "False")
            self.client = chromadb.Client(
                Settings(
                    anonymized_telemetry=False,
                    is_persistent=False,
                    persist_directory=str(settings.chroma_persist_dir),
                )
            )
            self.collection = self.client.get_or_create_collection(
                "health_knowledge", embedding_function=self._embed
            )
            self._load_documents()
        except Exception as e:
            logger.error(f"Chroma init failed, using fallback retrieval: {e}")
            self.client = None
            self.collection = None

    def _load_documents(self):
        docs = []
        ids = []
        metadatas = []
        for lang, symptom_map in self.loader.symptoms_db.items():
            for name, payload in symptom_map.items():
                ids.append(f"{lang}-{name}")
                docs.append(payload.get("response", ""))
                metadatas.append({"lang": lang, "name": name})
        if docs and self.collection:
            try:
                self.collection.upsert(documents=docs, ids=ids, metadatas=metadatas)
            except Exception as e:
                logger.error(f"Failed to upsert docs into Chroma: {e}")
                self.collection = None

    def _text_to_vector(self, text: str) -> List[float]:
        tokens = re.findall(r"\w+", text.lower())
        vector = [0.0] * 16
        for token in tokens:
            vector[hash(token) % 16] += 1.0
        return vector

    def _embed(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []
        for text in texts:
            if text not in self.embedding_cache:
                self.embedding_cache[text] = self._text_to_vector(text)
            embeddings.append(self.embedding_cache[text])
        return embeddings

    async def get_context(self, query: str, language: str) -> Tuple[List[str], str]:
        """Return relevant context and source label."""
        if self.collection:
            try:
                res = self.collection.query(query_texts=[query], n_results=self.top_k)
                contexts = res.get("documents", [[]])[0]
                return contexts, "chroma"
            except Exception as e:
                logger.error(f"Chroma query failed: {e}")

        # Fallback: pick top symptom responses by simple match
        fallback = self.loader.get_symptoms_for_language(language) or {}
        contexts = []
        q = query.lower()
        for symptom, data in fallback.items():
            if symptom.lower() in q or data.get("symptom", "").lower() in q:
                contexts.append(data.get("response", ""))
        return contexts[: self.top_k], "fallback"


retrieval_service = RetrievalService(health_data)
