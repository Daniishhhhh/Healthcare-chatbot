from __future__ import annotations

import re
from typing import Literal

Route = Literal["emergency", "medical", "scheme", "hospital"]


class TaskRouter:
    """Lightweight rule-based router for incoming queries."""

    def __init__(self):
        self.emergency_keywords = [
            "heart attack",
            "stroke",
            "chest pain",
            "breath",
            "bleeding",
            "unconscious",
            "सांस",
            "सीने",
            "दिल का दौरा",
            "ଶ୍ୱାସ",
            "ଛାତି",
        ]
        self.scheme_keywords = [
            "scheme",
            "insurance",
            "coverage",
            "ayushman",
            "pmjay",
            "plan",
            "benefit",
        ]
        self.hospital_keywords = [
            "hospital",
            "clinic",
            "phc",
            "chc",
            "doctor near",
            "appointment",
            "location",
        ]

    def route(self, text: str) -> Route:
        t = text.lower()

        if any(word in t for word in self.emergency_keywords):
            return "emergency"
        if any(word in t for word in self.scheme_keywords):
            return "scheme"
        if any(word in t for word in self.hospital_keywords):
            return "hospital"
        return "medical"


task_router = TaskRouter()
