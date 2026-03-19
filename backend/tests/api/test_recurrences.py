import uuid


class TestGetRecurrence:
    def test_not_found(self, client, sample_video):
        """GET recurrence returns 404 when no recurrence is set."""
        response = client.get(f"/api/videos/{sample_video.id}/recurrence")

        assert response.status_code == 404

    def test_found(self, client, sample_video):
        """GET recurrence returns 200 after recurrence is created."""
        client.put(
            f"/api/videos/{sample_video.id}/recurrence",
            json={"recurrence_type": "daily"},
        )

        response = client.get(f"/api/videos/{sample_video.id}/recurrence")

        assert response.status_code == 200
        assert response.json()["recurrence_type"] == "daily"


class TestUpsertRecurrence:
    def test_create_daily(self, client, sample_video):
        """PUT recurrence creates a daily recurrence and returns 200."""
        response = client.put(
            f"/api/videos/{sample_video.id}/recurrence",
            json={"recurrence_type": "daily"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["recurrence_type"] == "daily"

    def test_update(self, client, sample_video):
        """PUT recurrence updates existing recurrence."""
        client.put(
            f"/api/videos/{sample_video.id}/recurrence",
            json={"recurrence_type": "daily"},
        )

        response = client.put(
            f"/api/videos/{sample_video.id}/recurrence",
            json={
                "recurrence_type": "weekly",
                "weekdays": ["mon", "wed", "fri"],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["recurrence_type"] == "weekly"
        assert set(data["weekdays"]) == {"mon", "wed", "fri"}


class TestDeleteRecurrence:
    def test_delete(self, client, sample_video):
        """DELETE recurrence returns 204."""
        client.put(
            f"/api/videos/{sample_video.id}/recurrence",
            json={"recurrence_type": "daily"},
        )

        response = client.delete(f"/api/videos/{sample_video.id}/recurrence")

        assert response.status_code == 204

    def test_not_found(self, client, sample_video):
        """DELETE recurrence returns 404 when no recurrence exists."""
        response = client.delete(f"/api/videos/{sample_video.id}/recurrence")

        assert response.status_code == 404
