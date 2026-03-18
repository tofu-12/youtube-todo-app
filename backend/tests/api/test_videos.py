import uuid


class TestListVideos:
    def test_empty(self, client):
        """GET /api/videos returns empty list when no videos exist."""
        response = client.get("/api/videos")

        assert response.status_code == 200
        assert response.json() == []

    def test_with_videos(self, client, sample_video):
        """GET /api/videos returns list of videos."""
        response = client.get("/api/videos")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == str(sample_video.id)
        assert data[0]["name"] == sample_video.name


class TestCreateVideo:
    def test_create_minimal(self, client):
        """POST /api/videos with required fields only returns 201."""
        payload = {"name": "Test Video", "url": "https://youtube.com/watch?v=test"}

        response = client.post("/api/videos", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Video"
        assert data["url"] == "https://youtube.com/watch?v=test"
        assert data["tags"] == []

    def test_create_with_tags(self, client):
        """POST /api/videos with tag_names returns 201 with tags."""
        payload = {
            "name": "Tagged Video",
            "url": "https://youtube.com/watch?v=tagged",
            "tag_names": ["yoga", "stretch"],
        }

        response = client.post("/api/videos", json=payload)

        assert response.status_code == 201
        data = response.json()
        tag_names = [t["name"] for t in data["tags"]]
        assert "yoga" in tag_names
        assert "stretch" in tag_names


class TestGetVideo:
    def test_found(self, client, sample_video):
        """GET /api/videos/{video_id} returns 200 for existing video."""
        response = client.get(f"/api/videos/{sample_video.id}")

        assert response.status_code == 200
        assert response.json()["id"] == str(sample_video.id)

    def test_not_found(self, client):
        """GET /api/videos/{video_id} returns 404 for non-existent video."""
        response = client.get(f"/api/videos/{uuid.uuid4()}")

        assert response.status_code == 404


class TestUpdateVideo:
    def test_update_name(self, client, sample_video):
        """PUT /api/videos/{video_id} updates and returns 200."""
        response = client.put(
            f"/api/videos/{sample_video.id}",
            json={"name": "Updated Name", "url": sample_video.url},
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_not_found(self, client):
        """PUT /api/videos/{video_id} returns 404 for non-existent video."""
        response = client.put(
            f"/api/videos/{uuid.uuid4()}",
            json={"name": "No Video"},
        )

        assert response.status_code == 404


class TestDeleteVideo:
    def test_delete(self, client, sample_video):
        """DELETE /api/videos/{video_id} returns 204."""
        response = client.delete(f"/api/videos/{sample_video.id}")

        assert response.status_code == 204

    def test_not_found(self, client):
        """DELETE /api/videos/{video_id} returns 404 for non-existent video."""
        response = client.delete(f"/api/videos/{uuid.uuid4()}")

        assert response.status_code == 404
