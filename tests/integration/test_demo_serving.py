# tests/integration/test_demo_serving.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.mark.offline
def test_root_serves_inspire_mock():
    """Verifikasi endpoint root (/) menyajikan mock INSPIRE UNSRAT dengan asset terisolasi."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Portal INSPIRE - Universitas Sam Ratulangi" in response.text
    assert 'src="/inspire-unsrat-ac-id.html"' in response.text
    assert 'id="rag-chatbot-widget"' in response.text
    assert '/static/demo/inspire/js/inspire.js' in response.text
    assert '/static/demo/inspire/css/inspire.css' in response.text
    # Welcome card INSPIRE
    assert "SELAMAT DATANG" in response.text
    assert "Panduan Cara Bertanya" in response.text
    assert 'id="rag-guide-toggle-btn"' in response.text
    assert 'id="rag-guide-modal"' in response.text
    assert "rag-chip-btn" in response.text

@pytest.mark.offline
def test_unsratacid_serves_legacy_mock():
    """Verifikasi endpoint /unsratacid menyajikan mock legacy unsrat.ac.id 100% utuh tanpa perubahan."""
    response = client.get("/unsratacid")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Universitas Sam Ratulangi | Official Website" in response.text
    assert 'src="/unsrat-ac-id.html"' in response.text
    assert 'id="rag-chatbot-widget"' in response.text
    assert '/static/demo/unsratacid/js/unsratacid.js' in response.text
    assert '/static/demo/unsratacid/css/unsratacid.css' in response.text
    # Welcome card legacy
    assert "SELAMAT DATANG" in response.text
    assert "Syarat cuti akademik?" in response.text
    assert "rag-chip-btn" in response.text
    assert "rag-guide-drawer" not in response.text

@pytest.mark.offline
def test_raw_html_endpoints():
    """Verifikasi endpoint raw HTML untuk kedua iframe background."""
    resp_inspire = client.get("/inspire-unsrat-ac-id.html")
    assert resp_inspire.status_code == 200
    assert "text/html" in resp_inspire.headers["content-type"]

    resp_unsrat = client.get("/unsrat-ac-id.html")
    assert resp_unsrat.status_code == 200
    assert "text/html" in resp_unsrat.headers["content-type"]


