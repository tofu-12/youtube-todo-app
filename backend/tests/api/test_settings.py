class TestGetTimezones:
    def test_get_timezones(self, client):
        """GET /api/settings/timezones returns a list of timezone options."""
        response = client.get("/api/settings/timezones")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        values = [item["value"] for item in data]
        assert "Asia/Tokyo" in values

    def test_timezone_option_has_value_and_label(self, client):
        """Each timezone option has value and label fields."""
        response = client.get("/api/settings/timezones")

        data = response.json()
        for item in data:
            assert "value" in item
            assert "label" in item


class TestGetSettings:
    def test_get_default(self, client):
        """GET /api/settings returns default settings."""
        response = client.get("/api/settings")

        assert response.status_code == 200
        data = response.json()
        assert data["timezone"] == "Asia/Tokyo"
        assert data["day_change_time"] == "00:00:00"
        assert data["workout_history_expires_days"] == 90


class TestUpdateSettings:
    def test_update_timezone(self, client):
        """PUT /api/settings updates timezone."""
        response = client.put(
            "/api/settings",
            json={"timezone": "America/New_York"},
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

    def test_update_workout_history_expires_days(self, client):
        """PUT /api/settings updates workout_history_expires_days."""
        response = client.put(
            "/api/settings",
            json={"workout_history_expires_days": 180},
        )

        assert response.status_code == 200
        assert response.json()["workout_history_expires_days"] == 180

    def test_workout_history_expires_days_too_low(self, client):
        """PUT /api/settings with expires_days=0 returns 422."""
        response = client.put(
            "/api/settings",
            json={"workout_history_expires_days": 0},
        )

        assert response.status_code == 422

    def test_workout_history_expires_days_too_high(self, client):
        """PUT /api/settings with expires_days=366 returns 422."""
        response = client.put(
            "/api/settings",
            json={"workout_history_expires_days": 366},
        )

        assert response.status_code == 422
