from datetime import date, timedelta


class TestTodayVideos:
    def test_empty(self, client):
        """GET /api/today returns empty list when nothing is scheduled."""
        response = client.get("/api/today")

        assert response.status_code == 200
        assert response.json() == []

    def test_with_scheduled(self, client, db):
        """GET /api/today returns videos scheduled for today."""
        create_resp = client.post(
            "/api/videos",
            json={"name": "Daily Video", "url": "https://youtube.com/watch?v=daily"},
        )
        video_id = create_resp.json()["id"]

        # Set next_scheduled_date to today via direct DB update
        from app.models import Video

        video = db.get(Video, video_id)
        video.next_scheduled_date = date.today()
        db.flush()

        response = client.get("/api/today")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        video_ids = [v["id"] for v in data]
        assert video_id in video_ids


class TestOverdueVideos:
    def test_empty(self, client):
        """GET /api/overdue returns empty list when nothing is overdue."""
        response = client.get("/api/overdue")

        assert response.status_code == 200
        assert response.json() == []

    def test_with_overdue(self, client, db):
        """GET /api/overdue returns videos with past scheduled dates."""
        # Create a video
        create_resp = client.post(
            "/api/videos",
            json={
                "name": "Overdue Video",
                "url": "https://youtube.com/watch?v=overdue",
            },
        )
        video_id = create_resp.json()["id"]

        # Set next_scheduled_date to yesterday via direct DB update
        from app.models import Video

        yesterday = date.today() - timedelta(days=1)
        video = db.get(Video, video_id)
        video.next_scheduled_date = yesterday
        db.flush()

        response = client.get("/api/overdue")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        video_ids = [v["id"] for v in data]
        assert video_id in video_ids
