# tests/integration/test_demo_serving.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.mark.offline
def test_root_serves_inspire_mock():
    """Verifikasi endpoint root (/) dan (/inspire) menyajikan mock INSPIRE UNSRAT dengan asset terisolasi."""
    for path in ["/", "/inspire"]:
        response = client.get(path)
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Portal INSPIRE - Universitas Sam Ratulangi" in response.text
        assert 'src="/static/inspire/background.html"' in response.text
        assert 'id="rag-chatbot-widget"' in response.text
        assert '/static/inspire/js/inspire.js' in response.text
        assert '/static/inspire/css/inspire.css' in response.text
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
    assert 'src="/static/unsratacid/background.html"' in response.text
    assert 'id="rag-chatbot-widget"' in response.text
    assert '/static/unsratacid/js/unsratacid.js' in response.text
    assert '/static/unsratacid/css/unsratacid.css' in response.text
    # Welcome card legacy
    assert "SELAMAT DATANG" in response.text
    assert "Syarat cuti akademik?" in response.text
    assert "rag-chip-btn" in response.text
    assert "rag-guide-drawer" not in response.text

@pytest.mark.offline
def test_raw_html_endpoints():
    """Verifikasi endpoint raw HTML untuk kedua iframe background (kompatibilitas)."""
    resp_inspire = client.get("/inspire-unsrat-ac-id.html")
    assert resp_inspire.status_code == 200
    assert "text/html" in resp_inspire.headers["content-type"]

    resp_unsrat = client.get("/unsrat-ac-id.html")
    assert resp_unsrat.status_code == 200
    assert "text/html" in resp_unsrat.headers["content-type"]

@pytest.mark.offline
def test_evaluation_page_served():
    """Verifikasi endpoint /evaluation menyajikan dashboard evaluasi dengan benar."""
    resp_eval = client.get("/evaluation")
    assert resp_eval.status_code == 200
    assert "text/html" in resp_eval.headers["content-type"]
    assert "Evaluasi RAGAS | Chatbot UNSRAT" in resp_eval.text
    assert "/static/evaluation/js/evaluation.js" in resp_eval.text

@pytest.mark.offline
def test_dev_page_served():
    """Verifikasi endpoint /dev menyajikan developer control center dengan benar."""
    resp_dev = client.get("/dev")
    assert resp_dev.status_code == 200
    assert "text/html" in resp_dev.headers["content-type"]
    assert "Dev Control Panel" in resp_dev.text or "Developer" in resp_dev.text
    assert "/static/dev/js/dev.js" in resp_dev.text

@pytest.mark.offline
def test_testing_page_served():
    """Verifikasi endpoint /testing menyajikan SPA testing interface dengan benar."""
    resp_testing = client.get("/testing")
    assert resp_testing.status_code == 200
    assert "text/html" in resp_testing.headers["content-type"]
    assert "Asisten Informasi Akademik UNSRAT" in resp_testing.text
    assert "/static/testing/js/testing.js" in resp_testing.text

@pytest.mark.offline
def test_all_static_assets_served():
    """Verifikasi seluruh file CSS & JS utama dari ke-5 modul disajikan dengan 200 OK."""
    assets = [
        "/static/inspire/css/inspire.css",
        "/static/inspire/js/inspire.js",
        "/static/unsratacid/css/unsratacid.css",
        "/static/unsratacid/js/unsratacid.js",
        "/static/evaluation/js/evaluation.js",
        "/static/dev/js/dev.js",
        "/static/testing/js/testing.js",
        "/static/assets/logo-unsrat.png"
    ]
    for asset in assets:
        resp = client.get(asset)
        assert resp.status_code == 200, f"Asset gagal dimuat: {asset}"



