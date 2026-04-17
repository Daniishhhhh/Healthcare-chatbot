from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

try:
    from openai import AsyncAzureOpenAI
except Exception:  # pragma: no cover - openai optional in tests
    AsyncAzureOpenAI = None

from app.core.config import settings
from app.services.cache_service import TTLCache

logger = logging.getLogger(__name__)


class LLMService:
    """Azure OpenAI wrapper with cache, retry, and timeout safeguards."""

    def __init__(self):
        self.cache = TTLCache(ttl_seconds=settings.cache_ttl_seconds)
        self.client = None
        if AsyncAzureOpenAI and settings.azure_api_key and settings.azure_endpoint:
            try:
                self.client = AsyncAzureOpenAI(
                    api_key=settings.azure_api_key,
                    api_version="2024-02-15-preview",
                    azure_endpoint=settings.azure_endpoint,
                )
            except Exception as e:
                logger.error(f"Failed to init Azure OpenAI client: {e}")
                self.client = None
        else:
            logger.warning("Azure OpenAI not configured; using fallback responses.")

    async def generate(self, prompt: str, language: str) -> str:
        cache_key = f"{language}:{prompt}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        if not self.client or not settings.azure_deployment:
            return ""

        attempts = settings.retry_attempts
        delays = [0, 2, 5]

        for attempt in range(attempts):
            try:
                await asyncio.sleep(delays[attempt])
                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=settings.azure_deployment,
                        temperature=0.2,
                        max_tokens=350,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a concise, safe rural healthcare assistant. Answer in the user's language with brief steps and caution. Avoid diagnostics; encourage professional consultation.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                    ),
                    timeout=settings.llm_timeout_seconds,
                )
                text = response.choices[0].message.content
                self.cache.set(cache_key, text)
                return text
            except asyncio.TimeoutError:
                logger.warning("LLM timeout; retrying with backoff")
            except Exception as e:
                logger.error(f"LLM call failed (attempt {attempt+1}): {e}")

        return ""


llm_service = LLMService()
