class TestGetSettings:
    def test_get_default(self, client):
        """GET /api/settings returns default settings."""
        response = client.get("/api/settings")

        assert response.status_code == 200
        data = response.json()
        assert data["timezone"] == "Asia/Tokyo"
        assert data["day_change_time"] == "00:00:00"


class TestUpdateSettings:
    def test_update_timezone(self, client):
        """PUT /api/settings updates timezone."""
        response = client.put(
            "/api/settings",
            json={"timezone": "America/New_York", "day_change_time": "00:00:00"},
        )

        assert response.status_code == 200
        assert response.json()["timezone"] == "America/New_York"

    def test_invalid_timezone(self, client):
        """PUT /api/settings with invalid timezone returns 400."""
        response = client.put(
            "/api/settings",
            json={"timezone": "Invalid/Timezone"},
        )

        assert response.status_code == 400
