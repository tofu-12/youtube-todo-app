class TestListTags:
    def test_empty_when_no_tags(self, client):
        """GET /api/tags returns empty list when user has no tags."""
        response = client.get("/api/tags")

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_created_tags(self, client, sample_user, tag_factory):
        """GET /api/tags returns tags after creation."""
        tag_factory(sample_user.id, name="chest")
        tag_factory(sample_user.id, name="back")

        response = client.get("/api/tags")

        assert response.status_code == 200
        names = {t["name"] for t in response.json()}
        assert names == {"chest", "back"}

    def test_other_user_tags_not_visible(
        self, other_client, sample_user, tag_factory
    ):
        """GET /api/tags does not return another user's tags."""
        tag_factory(sample_user.id, name="secret")

        response = other_client.get("/api/tags")

        assert response.status_code == 200
        assert response.json() == []
