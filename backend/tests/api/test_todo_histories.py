import uuid
from datetime import date


class TestListTodoHistories:
    def test_empty(self, client):
        """GET /api/todo-histories returns empty list."""
        response = client.get("/api/todo-histories")

        assert response.status_code == 200
        assert response.json() == []

    def test_with_date_filter(self, client, sample_video):
        """GET /api/todo-histories filters by scheduled_date."""
        target_date = "2026-03-19"
        client.post(
            "/api/todo-histories",
            json={
                "video_id": str(sample_video.id),
                "scheduled_date": target_date,
                "status": "completed",
            },
        )
        # Create another entry on a different date
        client.post(
            "/api/todo-histories",
            json={
                "video_id": str(sample_video.id),
                "scheduled_date": "2026-03-20",
                "status": "skipped",
                "next_scheduled_date": "2026-03-25",
            },
        )

        response = client.get(
            "/api/todo-histories", params={"scheduled_date": target_date}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["scheduled_date"] == target_date


class TestCreateTodoHistory:
    def test_create_completed(self, client, sample_video):
        """POST /api/todo-histories with status completed returns 201."""
        payload = {
            "video_id": str(sample_video.id),
            "scheduled_date": "2026-03-19",
            "status": "completed",
        }

        response = client.post("/api/todo-histories", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "completed"
        assert data["video_id"] == str(sample_video.id)

    def test_create_with_nonexistent_video(self, client):
        """POST /api/todo-histories with nonexistent video_id returns 404."""
        payload = {
            "video_id": str(uuid.uuid4()),
            "scheduled_date": "2026-03-19",
            "status": "completed",
        }

        response = client.post("/api/todo-histories", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Video not found"

    def test_create_skipped_updates_next_scheduled_date(
        self, client, sample_video
    ):
        """POST /api/todo-histories with skipped updates video next_scheduled_date."""
        payload = {
            "video_id": str(sample_video.id),
            "scheduled_date": "2026-03-19",
            "status": "skipped",
            "next_scheduled_date": "2026-03-25",
        }

        response = client.post("/api/todo-histories", json=payload)

        assert response.status_code == 201
        assert response.json()["status"] == "skipped"

        video_resp = client.get(f"/api/videos/{sample_video.id}")
        assert video_resp.json()["next_scheduled_date"] == "2026-03-25"

    def test_create_skipped_without_next_date_returns_422(
        self, client, sample_video
    ):
        """POST /api/todo-histories with skipped but no next_scheduled_date returns 422."""
        payload = {
            "video_id": str(sample_video.id),
            "scheduled_date": "2026-03-19",
            "status": "skipped",
        }

        response = client.post("/api/todo-histories", json=payload)

        assert response.status_code == 422


class TestDeleteTodoHistory:
    def test_delete(self, client, sample_video):
        """DELETE /api/todo-histories/{entry_id} returns 204."""
        create_resp = client.post(
            "/api/todo-histories",
            json={
                "video_id": str(sample_video.id),
                "scheduled_date": "2026-03-19",
                "status": "completed",
            },
        )
        entry_id = create_resp.json()["id"]

        response = client.delete(f"/api/todo-histories/{entry_id}")

        assert response.status_code == 204

    def test_not_found(self, client):
        """DELETE /api/todo-histories/{entry_id} returns 404."""
        response = client.delete(f"/api/todo-histories/{uuid.uuid4()}")

        assert response.status_code == 404
