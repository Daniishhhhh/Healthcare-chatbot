import json
from pathlib import Path

from app.services.health_data_loader import HealthDataLoader


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_health_data_loader_reads_files(tmp_path):
    data_dir = tmp_path / "data"

    _write_json(data_dir / "health" / "symptoms_english.json", {"fever": "rest"})
    _write_json(data_dir / "health" / "symptoms_hindi.json", {"बुखार": "आराम करें"})
    _write_json(data_dir / "health" / "symptoms_odia.json", {"ଜ୍ୱର": "ବିଶ୍ରାମ ନିଅନ୍ତୁ"})
    _write_json(
        data_dir / "health" / "emergency_protocols.json",
        {"emergency_keywords": {"en": ["chest pain"]}},
    )
    _write_json(
        data_dir / "clinics" / "asha_workers.json",
        {"contacts": {"kalahandi": {"name": "Sunita"}}},
    )
    _write_json(
        data_dir / "health" / "seasonal_alerts.json",
        {"seasonal_alerts": [{"season": "monsoon"}]},
    )

    loader = HealthDataLoader(str(data_dir))

    assert loader.get_symptoms_for_language("en") == {"fever": "rest"}
    assert loader.get_symptoms_for_language("hi") == {"बुखार": "आराम करें"}
    assert loader.get_symptoms_for_language("or") == {"ଜ୍ୱର": "ବିଶ୍ରାମ ନିଅନ୍ତୁ"}
    assert loader.get_emergency_keywords("en") == ["chest pain"]
    assert loader.get_asha_contacts()["kalahandi"]["name"] == "Sunita"
    assert loader.get_seasonal_alerts() == [{"season": "monsoon"}]


def test_health_data_loader_fallbacks_when_missing_files(tmp_path):
    data_dir = tmp_path / "missing"

    loader = HealthDataLoader(str(data_dir))

    assert loader.get_symptoms_for_language("en") == {}
    assert loader.get_symptoms_for_language("hi") == {}
    assert loader.get_emergency_keywords("en")  # uses built-in fallback keywords
    assert loader.get_asha_contacts()  # uses built-in fallback contacts
    assert loader.get_seasonal_alerts() == []
