"""Integration tests for VideoTag CRUD operations."""

from app.crud.video_tag import get_video_tags, set_video_tags


class TestSetVideoTags:
    """Tests for set_video_tags."""

    def test_set_video_tags(self, db, sample_user, sample_video, tag_factory):
        """Setting tags on a video associates them correctly."""
        tag = tag_factory(sample_user.id)
        result = set_video_tags(
            db, sample_user.id, sample_video.id, [tag.id]
        )

        assert len(result) == 1
        assert result[0].id == tag.id

    def test_set_video_tags_replace(
        self, db, sample_user, sample_video, tag_factory
    ):
        """Setting new tags replaces the old ones."""
        tag1 = tag_factory(sample_user.id)
        tag2 = tag_factory(sample_user.id)

        set_video_tags(db, sample_user.id, sample_video.id, [tag1.id])
        result = set_video_tags(
            db, sample_user.id, sample_video.id, [tag2.id]
        )

        assert len(result) == 1
        assert result[0].id == tag2.id

    def test_set_video_tags_empty(
        self, db, sample_user, sample_video, tag_factory
    ):
        """Setting an empty list removes all tags."""
        tag = tag_factory(sample_user.id)
        set_video_tags(db, sample_user.id, sample_video.id, [tag.id])
        result = set_video_tags(db, sample_user.id, sample_video.id, [])

        assert result == []

    def test_get_video_tags_empty(self, db, sample_video):
        """Getting tags for a video with none returns empty list."""
        result = get_video_tags(db, sample_video.id)
        assert result == []

    def test_set_video_tags_multiple(
        self, db, sample_user, sample_video, tag_factory
    ):
        """Setting multiple tags on a video works correctly."""
        tag1 = tag_factory(sample_user.id)
        tag2 = tag_factory(sample_user.id)
        tag3 = tag_factory(sample_user.id)

        result = set_video_tags(
            db, sample_user.id, sample_video.id,
            [tag1.id, tag2.id, tag3.id],
        )

        assert len(result) == 3
        result_ids = {r.id for r in result}
        assert tag1.id in result_ids
        assert tag2.id in result_ids
        assert tag3.id in result_ids
