# tests/test_spa_serving.py
# Unit/Integration test untuk SPA Frontend serving
# Jalankan: pytest tests/test_spa_serving.py -v

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root_serves_index_html():
    """Verifikasi endpoint root (/) mengembalikan static/index.html dengan benar."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Asisten Informasi Akademik UNSRAT" in response.text
    assert '<script src="/static/js/app.js"></script>' in response.text

def test_static_files_js_app_served():
    """Verifikasi /static/js/app.js disajikan dengan status 200 dan tipe konten yang tepat."""
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"] or "text/plain" in response.headers["content-type"] or "javascript" in response.headers["content-type"]
    assert "isStreaming" in response.text
    assert "loadEvaluationData" in response.text
    assert "copyTableToClipboard" in response.text
