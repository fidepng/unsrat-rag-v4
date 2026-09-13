# tests/integration/test_demo_serving.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.mark.offline
def test_root_serves_inspire_mock():
    """Verifikasi endpoint root (/) menyajikan mock INSPIRE UNSRAT beserta chatbot widget."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Portal INSPIRE - Universitas Sam Ratulangi" in response.text
    assert 'src="/inspire-unsrat-ac-id.html"' in response.text
    assert 'id="rag-chatbot-widget"' in response.text
    assert '/static/demo/js/inspire-chat.js' in response.text
    assert '/static/demo/css/inspire-chat.css' in response.text
    assert 'rag-welcome-msg-wrapper' in response.text

@pytest.mark.offline
def test_unsratacid_serves_legacy_mock():
    """Verifikasi endpoint /unsratacid menyajikan mock legacy unsrat.ac.id tanpa perubahan."""
    response = client.get("/unsratacid")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Universitas Sam Ratulangi | Official Website" in response.text
    assert 'src="/unsrat-ac-id.html"' in response.text
    assert 'id="rag-chatbot-widget"' in response.text
    assert '/static/demo/js/chat-widget.js' in response.text
    assert '/static/demo/css/demo-modal.css' in response.text

@pytest.mark.offline
def test_raw_html_endpoints():
    """Verifikasi endpoint raw HTML untuk kedua iframe background."""
    resp_inspire = client.get("/inspire-unsrat-ac-id.html")
    assert resp_inspire.status_code == 200
    assert "text/html" in resp_inspire.headers["content-type"]

    resp_unsrat = client.get("/unsrat-ac-id.html")
    assert resp_unsrat.status_code == 200
    assert "text/html" in resp_unsrat.headers["content-type"]
