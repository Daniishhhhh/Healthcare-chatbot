# app/services/language_detector.py
import sys
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Language detection fallback (without langdetect dependency)
LANGUAGE_KEYWORDS = {
    "hi": ["बुखार", "सिरदर्द", "खांसी", "दर्द", "आपातकाल", "नमस्ते", "मुझे", "है", "के", "में"],
    "or": ["ଜ୍ୱର", "ମୁଣ୍ଡବିନ୍ଧା", "କାଶ", "ଦରଦ", "ଜରୁରୀକାଳୀନ", "ନମସ୍କାର", "ମୋର", "ଅଛି", "ପାଇଁ"],
    "en": ["fever", "headache", "cough", "pain", "emergency", "hello", "have", "is", "for", "help"]
}

def detect_language_with_confidence(text: str) -> tuple[str, float]:
    """
    Detect language with confidence score
    Returns (language_code, confidence_score)
    """
    if not text or not text.strip():
        return "en", 0.0
    
    text_lower = text.lower()
    scores = {"hi": 0, "or": 0, "en": 0}
    
    # Count matches for each language
    for lang, keywords in LANGUAGE_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                scores[lang] += 1
    
    # Find language with highest score
    max_lang = max(scores, key=scores.get)
    max_score = scores[max_lang]
    
    # Calculate confidence (simple heuristic)
    total_words = len(text.split())
    confidence = min(max_score / max(total_words, 1), 1.0)
    
    # Default to English if confidence is too low
    if confidence < 0.2:
        return "en", confidence
    
    return max_lang, confidence

def detect_language(text: str) -> str:
    """
    Detect language (simplified version)
    Returns language code only
    """
    lang, _ = detect_language_with_confidence(text)
    return lang
