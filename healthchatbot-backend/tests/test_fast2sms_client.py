from app.integrations.fast2sms_client import Fast2SMSClient


class DummyResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


def test_missing_api_key_returns_error():
    client = Fast2SMSClient("")

    result = client.send_sms("+911234567890", "hello")

    assert result["status"] == "error"
    assert result["status_code"] == 400
    assert "API key" in result["error"]


def test_send_sms_success(monkeypatch):
    sent_payload = {}

    def fake_post(url, data=None, headers=None):
        sent_payload["numbers"] = data["numbers"]
        sent_payload["message"] = data["message"]
        return DummyResponse(200, {"message": "ok"})

    monkeypatch.setattr("app.integrations.fast2sms_client.requests.post", fake_post)

    client = Fast2SMSClient("secret")
    result = client.send_sms("+911234567890", "ping")

    assert result["status"] == "success"
    assert result["response"] == {"message": "ok"}
    assert sent_payload["numbers"] == "1234567890"
    assert sent_payload["message"] == "ping"


def test_send_sms_handles_request_exception(monkeypatch):
    def fake_post(url, data=None, headers=None):
        raise RuntimeError("network down")

    monkeypatch.setattr("app.integrations.fast2sms_client.requests.post", fake_post)

    client = Fast2SMSClient("secret")
    result = client.send_sms("12345", "ping")

    assert result["status"] == "error"
    assert "network down" in result["error"]
