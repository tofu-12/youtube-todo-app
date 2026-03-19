import uuid


class TestListWorkoutHistories:
    def test_empty(self, client):
        """GET /api/workout-histories returns empty list."""
        response = client.get("/api/workout-histories")

        assert response.status_code == 200
        assert response.json() == []


class TestCreateWorkoutHistory:
    def test_create(self, client, sample_video):
        """POST /api/workout-histories returns 201 using user settings expires_days."""
        payload = {
            "video_id": str(sample_video.id),
        }

        response = client.post("/api/workout-histories", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["video_id"] == str(sample_video.id)
        assert "performed_date" in data
        assert "expires_date" in data

    def test_create_with_nonexistent_video(self, client):
        """POST /api/workout-histories with nonexistent video_id returns 404."""
        payload = {
            "video_id": str(uuid.uuid4()),
        }

        response = client.post("/api/workout-histories", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Video not found"

    def test_create_uses_user_settings_expires_days(self, client, sample_video):
        """POST /api/workout-histories uses the user's workout_history_expires_days setting."""
        # Update user setting to 30 days
        client.put(
            "/api/settings",
            json={"workout_history_expires_days": 30},
        )

        payload = {"video_id": str(sample_video.id)}
        response = client.post("/api/workout-histories", json=payload)

        assert response.status_code == 201
        data = response.json()
        from datetime import date, timedelta

        performed = date.fromisoformat(data["performed_date"])
        expires = date.fromisoformat(data["expires_date"])
        assert (expires - performed).days == 30


class TestDeleteWorkoutHistory:
    def test_delete(self, client, sample_video):
        """DELETE /api/workout-histories/{entry_id} returns 204."""
        create_resp = client.post(
            "/api/workout-histories",
            json={
                "video_id": str(sample_video.id),
            },
        )
        entry_id = create_resp.json()["id"]

        response = client.delete(f"/api/workout-histories/{entry_id}")

        assert response.status_code == 204

    def test_not_found(self, client):
        """DELETE /api/workout-histories/{entry_id} returns 404."""
        response = client.delete(f"/api/workout-histories/{uuid.uuid4()}")

        assert response.status_code == 404
