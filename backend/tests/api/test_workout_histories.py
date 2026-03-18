import uuid


class TestListWorkoutHistories:
    def test_empty(self, client):
        """GET /api/workout-histories returns empty list."""
        response = client.get("/api/workout-histories")

        assert response.status_code == 200
        assert response.json() == []


class TestCreateWorkoutHistory:
    def test_create(self, client, sample_video):
        """POST /api/workout-histories returns 201."""
        payload = {
            "video_id": str(sample_video.id),
            "expires_days": 3,
        }

        response = client.post("/api/workout-histories", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["video_id"] == str(sample_video.id)
        assert "performed_date" in data
        assert "expires_date" in data


class TestDeleteWorkoutHistory:
    def test_delete(self, client, sample_video):
        """DELETE /api/workout-histories/{entry_id} returns 204."""
        create_resp = client.post(
            "/api/workout-histories",
            json={
                "video_id": str(sample_video.id),
                "expires_days": 3,
            },
        )
        entry_id = create_resp.json()["id"]

        response = client.delete(f"/api/workout-histories/{entry_id}")

        assert response.status_code == 204

    def test_not_found(self, client):
        """DELETE /api/workout-histories/{entry_id} returns 404."""
        response = client.delete(f"/api/workout-histories/{uuid.uuid4()}")

        assert response.status_code == 404
