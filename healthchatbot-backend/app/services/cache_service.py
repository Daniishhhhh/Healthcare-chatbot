from __future__ import annotations

import time
from typing import Any, Dict, Optional


class TTLCache:
    """In-memory TTL cache with simple eviction."""

    def __init__(self, ttl_seconds: int = 600, max_items: int = 256):
        self.ttl_seconds = ttl_seconds
        self.max_items = max_items
        self._store: Dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None

        expires_at, value = entry
        if expires_at < time.time():
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any):
        if len(self._store) >= self.max_items:
            # Evict oldest item
            oldest_key = min(self._store.items(), key=lambda item: item[1][0])[0]
            self._store.pop(oldest_key, None)
        self._store[key] = (time.time() + self.ttl_seconds, value)

    def clear(self):
        self._store.clear()
