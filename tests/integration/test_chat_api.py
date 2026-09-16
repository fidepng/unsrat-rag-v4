import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app

client = TestClient(app, raise_server_exceptions=False)

@pytest.mark.offline
class TestChatAPI:
    @patch("app.get_response")
    def test_chat_endpoint_success(self, mock_get_response):
        # Mock SSE generator
        def sse_gen():
            yield "event: thinking\ndata: {}\n\n"
            yield "event: token\ndata: \"Berdasarkan pedoman akademik\"\n\n"
            yield "event: done\ndata: {}\n\n"
            
        mock_get_response.return_value = sse_gen()
        
        payload = {
            "query": "Berapa SKS?",
            "config": "b",
            "model": "google/gemma-4-31b-it",
            "chat_history": []
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        assert "event: token" in response.text
        assert "Berdasarkan pedoman akademik" in response.text

    @patch("app.get_response")
    def test_chat_endpoint_streaming_error_event(self, mock_get_response):
        # Mock generator returning a handled streaming error SSE event
        def sse_error_gen():
            yield "event: thinking\ndata: {}\n\n"
            yield 'data: {"type": "error", "message": "Terjadi kesalahan sistem. Coba lagi."}\n\n'
            
        mock_get_response.return_value = sse_error_gen()
        
        payload = {
            "query": "Berapa SKS?",
            "config": "b",
            "model": "google/gemma-4-31b-it",
            "chat_history": []
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        assert "Terjadi kesalahan sistem. Coba lagi." in response.text

    @patch("app.AVAILABLE_MODELS", new=object())
    def test_config_endpoint_internal_error_middleware(self):
        # Trigger an unhandled TypeError during JSON serialization in the route
        response = client.get("/api/config")
        assert response.status_code == 500
        json_data = response.json()
        assert "detail" in json_data
        assert "Terjadi kesalahan internal pada server" in json_data["detail"]


from src.config import DEV_ADMIN_KEY

@pytest.mark.offline
class TestDevAPI:
    @patch("app.IS_CLOUD_RUN", True)
    def test_dev_status_endpoint_unauthorized_on_cloud_run(self):
        response = client.get("/api/dev/status")
        assert response.status_code == 403
        assert "Akses ditolak" in response.json()["detail"]

    @patch("app.IS_CLOUD_RUN", True)
    def test_dev_status_endpoint_authorized_on_cloud_run(self):
        response = client.get("/api/dev/status", headers={"X-Admin-Key": DEV_ADMIN_KEY})
        assert response.status_code == 200
        data = response.json()
        assert "active_generator" in data
        assert "google_api_key_present" in data

    def test_dev_status_endpoint_authorized_on_local(self):
        # On local dev (IS_CLOUD_RUN=False), direct access without header is allowed
        response = client.get("/api/dev/status")
        assert response.status_code == 200
        data = response.json()
        assert "active_generator" in data
        assert "google_api_key_present" in data
        assert "is_cloud_run" in data

    @patch("app.preflight_check")
    def test_dev_preflight_endpoint(self, mock_preflight):
        mock_preflight.return_value = {"status": "ok", "google_api": True}
        response = client.get("/api/dev/preflight", headers={"X-Admin-Key": DEV_ADMIN_KEY})
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_dev_runs_endpoint(self):
        response = client.get("/api/dev/runs", headers={"X-Admin-Key": DEV_ADMIN_KEY})
        assert response.status_code == 200
        assert "runs" in response.json()

    def test_dev_activate_run_not_found(self):
        response = client.post(
            "/api/dev/runs/activate",
            json={"run_id": "nonexistent_run_999"},
            headers={"X-Admin-Key": DEV_ADMIN_KEY}
        )
        assert response.status_code == 404
        assert "tidak ditemukan" in response.json()["detail"]

    def test_dev_logs_endpoint(self):
        response = client.get("/api/dev/logs?lines=10", headers={"X-Admin-Key": DEV_ADMIN_KEY})
        assert response.status_code == 200
        data = response.json()
        assert "log_path" in data
        assert "lines" in data


@pytest.mark.offline
class TestSecurityAPI:
    def test_security_headers_present(self):
        response = client.get("/api/config")
        assert response.status_code == 200
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"

    def test_query_max_length_validation(self):
        payload = {
            "query": "A" * 1001,
            "config": "b",
            "chat_history": []
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 422

    def test_chat_history_max_length_validation(self):
        payload = {
            "query": "Halo",
            "config": "b",
            "chat_history": [{"role": "user", "content": "test"}] * 11
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 422

    @patch("app.get_response")
    def test_rate_limit_exceeded(self, mock_get_response):
        def sse_gen():
            yield "event: token\ndata: \"test\"\n\n"
        mock_get_response.return_value = sse_gen()

        # Send 5 requests (allowed)
        for i in range(5):
            res = client.post("/api/chat", json={"query": f"Test {i}"})
            assert res.status_code == 200

        # 6th request should be rate-limited
        res_blocked = client.post("/api/chat", json={"query": "Test 6"})
        assert res_blocked.status_code == 429

