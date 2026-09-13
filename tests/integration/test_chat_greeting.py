# tests/integration/test_chat_greeting.py
import json
import pytest
from fastapi.testclient import TestClient
from app import app
from src.chain import get_response

client = TestClient(app)

@pytest.mark.offline
def test_sync_greeting_via_get_response():
    """Verifikasi get_response (non-streaming) merespons sapaan murni seketika."""
    res = get_response("Halo!", config="b", chat_history=[], model_name="gemini-3.5-flash", streaming=False)
    assert isinstance(res, dict)
    assert "Asisten Akademik UNSRAT" in res["answer"]
    assert res["citation_sources"] == []
    assert res["retrieved_contexts"] == []
    assert res["found"] is True

@pytest.mark.offline
def test_streaming_greeting_api():
    """Verifikasi endpoint /api/chat SSE menghasilkan event token, citations kosong, dan done untuk sapaan."""
    payload = {
        "query": "Selamat pagi",
        "config": "b",
        "model": "gemini-3.5-flash",
        "chat_history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

    events = []
    for line in response.text.split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            events.append(json.loads(line[6:]))

    # Pastikan event token diterima dan memuat sapaan
    token_events = [e for e in events if e.get("type") == "token"]
    assert len(token_events) >= 1
    assert "Selamat pagi" in token_events[0]["content"]

    # Pastikan event citations kosong
    citation_events = [e for e in events if e.get("type") == "citations"]
    assert len(citation_events) >= 1
    assert citation_events[0]["sources"] == []

    # Pastikan event done diterima
    done_events = [e for e in events if e.get("type") == "done"]
    assert len(done_events) >= 1

@pytest.mark.offline
def test_streaming_closing_api():
    """Verifikasi ucapan terima kasih dibalas sama-sama via SSE."""
    payload = {
        "query": "Terima kasih banyak!",
        "config": "b",
        "model": "gemini-3.5-flash",
        "chat_history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200

    events = [json.loads(l.strip()[6:]) for l in response.text.split("\n") if l.strip().startswith("data: ")]
    token_text = "".join(e.get("content", "") for e in events if e.get("type") == "token")
    assert "Sama-sama" in token_text

@pytest.mark.offline
def test_streaming_identity_api():
    """Verifikasi pertanyaan siapa anda dijawab via SSE dengan perkenalan Asisten Akademik."""
    payload = {
        "query": "Siapa anda?",
        "config": "b",
        "model": "gemini-3.5-flash",
        "chat_history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200

    events = [json.loads(l.strip()[6:]) for l in response.text.split("\n") if l.strip().startswith("data: ")]
    token_text = "".join(e.get("content", "") for e in events if e.get("type") == "token")
    assert "Asisten Akademik UNSRAT" in token_text

@pytest.mark.offline
def test_streaming_capability_api():
    """Verifikasi pertanyaan apa yang bisa anda lakukan dijawab via SSE dengan daftar kapabilitas."""
    payload = {
        "query": "Apa yang bisa anda lakukan?",
        "config": "b",
        "model": "gemini-3.5-flash",
        "chat_history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200

    events = [json.loads(l.strip()[6:]) for l in response.text.split("\n") if l.strip().startswith("data: ")]
    token_text = "".join(e.get("content", "") for e in events if e.get("type") == "token")
    assert "KRS" in token_text
    assert "cuti akademik" in token_text

