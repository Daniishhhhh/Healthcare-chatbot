import pytest

from app.services.language_detector import (
    detect_language,
    detect_language_with_confidence,
)
from app.services.query_service import HealthQueryProcessor


@pytest.mark.asyncio
async def test_emergency_query_detection():
    processor = HealthQueryProcessor()

    result = await processor.process_query_async(
        "This is an emergency, need urgent help", "en"
    )

    assert result["intent"] == "emergency"
    assert result["emergency"] is True
    assert result["severity"] == "critical"
    assert "EMERGENCY" in result["response"]


@pytest.mark.asyncio
async def test_symptom_response_in_hindi():
    processor = HealthQueryProcessor()

    result = await processor.process_query_async("मुझे बुखार है", "hi")

    assert result["intent"] == "symptoms"
    assert result["emergency"] is False
    assert result["severity"] == "mild"
    assert "बुखार" in result["response"]


@pytest.mark.asyncio
async def test_general_response_defaults_to_english_text():
    processor = HealthQueryProcessor()

    result = await processor.process_query_async("Tell me more", "fr")

    assert result["intent"] == "general"
    assert result["emergency"] is False
    assert "health assistant" in result["response"]


def test_language_detection_high_confidence_hindi():
    lang, confidence = detect_language_with_confidence("मुझे खांसी और बुखार है")

    assert lang == "hi"
    assert confidence >= 0.2


def test_language_detection_defaults_to_english_when_uncertain():
    lang, confidence = detect_language_with_confidence("random text with no keywords")

    assert lang == "en"
    assert confidence == 0.0
    assert detect_language("random text with no keywords") == "en"
