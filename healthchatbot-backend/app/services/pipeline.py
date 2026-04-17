from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.core.session_manager import session_manager
from app.services.cache_service import TTLCache
from app.services.emergency_service import emergency_engine, escalate_to_asha
from app.services.health_data_loader import health_data
from app.services.language_detector import detect_language
from app.services.llm_service import llm_service
from app.services.retrieval_service import retrieval_service
from app.services.task_router import task_router

logger = logging.getLogger(__name__)

HOSPITAL_DIRECTORY = [
    {
        "name": "Kalahandi Primary Health Centre",
        "phone": "+91-9876543210",
        "location": "Bhawanipatna",
        "distance": "2.4 km",
        "map": "https://maps.google.com/?q=Bhawanipatna+PHC",
    },
    {
        "name": "Bhubaneswar Community Health Centre",
        "phone": "+91-9876543211",
        "location": "Bhubaneswar",
        "distance": "4.1 km",
        "map": "https://maps.google.com/?q=Bhubaneswar+CHC",
    },
    {
        "name": "Cuttack PHC",
        "phone": "+91-9876543212",
        "location": "Cuttack",
        "distance": "7.8 km",
        "map": "https://maps.google.com/?q=Cuttack+PHC",
    },
]


class AssistantOrchestrator:
    """End-to-end orchestration for a single-turn query."""

    def __init__(self):
        self.cache = TTLCache(ttl_seconds=settings.cache_ttl_seconds)

    async def handle_query(
        self,
        message: str,
        user_id: str,
        language: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        lang = language or detect_language(message)
        session = session_manager.get_session(user_id)
        session_manager.update_activity(user_id)
        if lang:
            session_manager.set_language(user_id, lang)

        cache_key = f"{lang}:{message.strip().lower()}"
        cached = self.cache.get(cache_key)
        if cached:
            cached_copy = dict(cached)
            cached_copy["cached"] = True
            return cached_copy

        route = task_router.route(message)
        emergency_eval = emergency_engine.assess(message)

        if emergency_eval["triggered"] or route == "emergency":
            session_manager.mark_emergency(user_id)
            response_text = emergency_engine.build_emergency_message(user_id, message)
            await escalate_to_asha(user_id, message, "scored_emergency")
            payload = self._build_response(
                response_text,
                intent="emergency",
                severity="critical",
                emergency=True,
                meta={"route": route, "emergency_score": emergency_eval["score"]},
            )
            self.cache.set(cache_key, payload)
            session_manager.add_to_history(user_id, message, response_text)
            return payload

        if route == "scheme":
            response_text = (
                "Available schemes: Ayushman Bharat (PM-JAY) for eligible families, "
                "Biju Swasthya Kalyan Yojana in Odisha, and free emergency transport via 108. "
                "Carry an ID and any previous prescriptions when visiting a facility."
            )
            payload = self._build_response(
                response_text,
                intent="scheme",
                severity="low",
                emergency=False,
                meta={"route": route},
            )
            self.cache.set(cache_key, payload)
            session_manager.add_to_history(user_id, message, response_text)
            return payload

        if route == "hospital":
            response_text = (
                "Here are nearby facilities. Call ahead, carry ID, and seek emergency help via 108 if needed."
            )
            payload = self._build_response(
                response_text,
                intent="hospital",
                severity="medium",
                emergency=False,
                meta={"route": route, "hospitals": HOSPITAL_DIRECTORY},
            )
            self.cache.set(cache_key, payload)
            session_manager.add_to_history(user_id, message, response_text)
            return payload

        contexts, source = await retrieval_service.get_context(message, lang)
        turns = (history or [])[-settings.max_history :]
        prompt = self._build_prompt(message, lang, contexts, turns)

        llm_answer = await llm_service.generate(prompt, lang)
        if not llm_answer:
            llm_answer = self._knowledge_base_fallback(message, lang)

        meta = {
            "route": route,
            "context_source": source,
            "context_used": bool(contexts),
            "emergency_score": emergency_eval["score"],
        }

        payload = self._build_response(
            llm_answer,
            intent="medical",
            severity="medium",
            emergency=False,
            meta=meta,
        )
        self.cache.set(cache_key, payload)
        session_manager.add_to_history(user_id, message, llm_answer)
        return payload

    def _build_prompt(
        self,
        message: str,
        language: str,
        contexts: List[str],
        history: List[Dict[str, str]],
    ) -> str:
        context_block = "\n".join(contexts) if contexts else "Use general first-aid guidance."
        history_block = "\n".join(
            f"{turn.get('role','user')}: {turn.get('content','')}" for turn in history
        )

        return (
            f"Language: {language}\n"
            "Respond briefly (120 words max) with numbered steps when needed.\n"
            "Avoid definitive diagnoses; encourage clinician follow-up.\n"
            "If anything sounds dangerous, add: 'If severe, call 108 immediately.'\n"
            f"Context:\n{context_block}\n"
            f"Recent conversation:\n{history_block}\n"
            f"User message: {message}"
        )

    def _knowledge_base_fallback(self, message: str, language: str) -> str:
        symptoms = health_data.get_symptoms_for_language(language)
        text = message.lower()
        best_match = None
        for name, data in symptoms.items():
            if name.lower() in text or data.get("symptom", "").lower() in text:
                best_match = data
                break

        if best_match:
            return best_match.get("response", settings.fallback_response)

        return (
            "I could not fetch a detailed answer right now. "
            "Monitor symptoms, stay hydrated, and contact a clinician if you feel worse."
        )

    def _build_response(
        self,
        text: str,
        intent: str,
        severity: str,
        emergency: bool,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return {
            "response": text,
            "intent": intent,
            "severity": severity,
            "emergency": emergency,
            "meta": meta or {},
            "cached": False,
        }


assistant_orchestrator = AssistantOrchestrator()
