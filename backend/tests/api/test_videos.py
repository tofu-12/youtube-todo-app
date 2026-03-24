import datetime
import uuid

from app.crud.video_tag import set_video_tags


class TestListVideos:
    def test_empty(self, client):
        """GET /api/videos returns empty paginated response when no videos exist."""
        response = client.get("/api/videos")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["skip"] == 0
        assert data["limit"] == 20

    def test_with_videos(self, client, sample_video):
        """GET /api/videos returns paginated list of videos."""
        response = client.get("/api/videos")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == str(sample_video.id)
        assert data["items"][0]["name"] == sample_video.name


class TestListVideosFilter:
    def test_filter_by_name(self, client, sample_user, video_factory):
        """Filtering by name returns only matching videos."""
        video_factory(sample_user.id, name="Morning Yoga")
        video_factory(sample_user.id, name="Evening Stretch")
        video_factory(sample_user.id, name="HIIT Workout")

        response = client.get("/api/videos", params={"name": "yoga"})

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Morning Yoga"

    def test_filter_by_tag_names_and(
        self, db, client, sample_user, video_factory, tag_factory
    ):
        """Filtering by tag_names returns videos having ALL specified tags."""
        tag_yoga = tag_factory(sample_user.id, name="yoga")
        tag_stretch = tag_factory(sample_user.id, name="stretch")
        tag_hiit = tag_factory(sample_user.id, name="hiit")

        v1 = video_factory(sample_user.id, name="Video A")
        v2 = video_factory(sample_user.id, name="Video B")
        v3 = video_factory(sample_user.id, name="Video C")

        set_video_tags(db, sample_user.id, v1.id, [tag_yoga.id, tag_stretch.id])
        set_video_tags(db, sample_user.id, v2.id, [tag_yoga.id])
        set_video_tags(db, sample_user.id, v3.id, [tag_hiit.id])

        response = client.get(
            "/api/videos",
            params={"tag_names": ["yoga", "stretch"]},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Video A"

    def test_filter_by_scheduled_status_overdue(
        self, client, sample_user, video_factory
    ):
        """Filtering by scheduled_status=overdue returns past-due videos."""
        today = datetime.date.today()
        video_factory(
            sample_user.id,
            name="Overdue",
            next_scheduled_date=today - datetime.timedelta(days=3),
        )
        video_factory(
            sample_user.id,
            name="Today",
            next_scheduled_date=today,
        )
        video_factory(sample_user.id, name="No Date")

        response = client.get(
            "/api/videos", params={"scheduled_status": "overdue"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Overdue"

    def test_filter_by_scheduled_status_unscheduled(
        self, client, sample_user, video_factory
    ):
        """Filtering by scheduled_status=unscheduled returns videos without dates."""
        today = datetime.date.today()
        video_factory(
            sample_user.id,
            name="Scheduled",
            next_scheduled_date=today,
        )
        video_factory(sample_user.id, name="Unscheduled")

        response = client.get(
            "/api/videos", params={"scheduled_status": "unscheduled"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Unscheduled"


class TestListVideosSort:
    def test_sort_by_name_asc(self, client, sample_user, video_factory):
        """Sorting by name ascending returns videos in alphabetical order."""
        video_factory(sample_user.id, name="Charlie")
        video_factory(sample_user.id, name="Alice")
        video_factory(sample_user.id, name="Bob")

        response = client.get(
            "/api/videos",
            params={"sort_field": "name", "sort_order": "asc"},
        )

        assert response.status_code == 200
        data = response.json()
        names = [v["name"] for v in data["items"]]
        assert names == ["Alice", "Bob", "Charlie"]

    def test_sort_nulls_last(self, client, sample_user, video_factory):
        """NULL values in sort field are placed at the end."""
        today = datetime.date.today()
        video_factory(
            sample_user.id,
            name="Has Date",
            next_scheduled_date=today,
        )
        video_factory(sample_user.id, name="No Date")

        response = client.get(
            "/api/videos",
            params={
                "sort_field": "next_scheduled_date",
                "sort_order": "asc",
            },
        )

        assert response.status_code == 200
        data = response.json()
        names = [v["name"] for v in data["items"]]
        assert names == ["Has Date", "No Date"]


class TestListVideosPagination:
    def test_pagination(self, client, sample_user, video_factory):
        """Pagination with skip and limit returns correct subset."""
        for i in range(5):
            video_factory(sample_user.id, name=f"Video {i}")

        response = client.get(
            "/api/videos",
            params={"skip": 2, "limit": 2, "sort_field": "created_at", "sort_order": "asc"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["skip"] == 2
        assert data["limit"] == 2

    def test_pagination_total_with_filter(
        self, client, sample_user, video_factory
    ):
        """Total count reflects filtered results, not all videos."""
        video_factory(sample_user.id, name="Yoga Flow")
        video_factory(sample_user.id, name="Yoga Stretch")
        video_factory(sample_user.id, name="HIIT Workout")

        response = client.get(
            "/api/videos", params={"name": "yoga", "limit": 1}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 1


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

    def test_create_with_next_scheduled_date(self, client):
        """POST /api/videos with next_scheduled_date returns 201."""
        payload = {
            "name": "Scheduled Video",
            "url": "https://youtube.com/watch?v=sched",
            "next_scheduled_date": "2026-04-01",
        }

        response = client.post("/api/videos", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["next_scheduled_date"] == "2026-04-01"

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
            json={"name": "Updated Name"},
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_update_next_scheduled_date(self, client, sample_video):
        """PUT /api/videos/{video_id} with next_scheduled_date updates it."""
        response = client.put(
            f"/api/videos/{sample_video.id}",
            json={"next_scheduled_date": "2026-05-15"},
        )

        assert response.status_code == 200
        assert response.json()["next_scheduled_date"] == "2026-05-15"

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
