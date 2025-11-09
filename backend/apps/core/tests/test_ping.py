from django.test import TestCase
from django.urls import reverse

class PingTest(TestCase):
    def test_ping_returns_ok_and_request_id(self):
        resp = self.client.get(reverse("api-ping"), HTTP_ACCEPT="application/json")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "ping" in data["data"]
        assert data["data"].get("request_id") is not None
