"""Integration tests for Tag CRUD operations."""

import uuid

from app.crud.schemas.tag import TagInsert
from app.crud.tag import create_tag, delete_tag, get_or_create_tag, get_tags


class TestCreateTag:
    """Tests for create_tag."""

    def test_create_tag(self, db, sample_user):
        """Creating a tag stores it correctly."""
        data = TagInsert(user_id=sample_user.id, name="yoga")
        result = create_tag(db, data)

        assert result.name == "yoga"
        assert result.user_id == sample_user.id
        assert result.id is not None


class TestGetTags:
    """Tests for get_tags."""

    def test_get_tags(self, db, sample_user, tag_factory):
        """Getting tags for a user returns all their tags."""
        tag_factory(sample_user.id, name="yoga")
        tag_factory(sample_user.id, name="hiit")

        result = get_tags(db, sample_user.id)
        assert len(result) == 2

    def test_get_tags_empty(self, db, user_factory):
        """Getting tags for a user with none returns empty list."""
        user = user_factory()
        result = get_tags(db, user.id)
        assert result == []

    def test_get_tags_user_isolation(
        self, db, sample_user, tag_factory, user_factory
    ):
        """Tags from other users are not included."""
        tag_factory(sample_user.id, name="yoga")
        other_user = user_factory()
        tag_factory(other_user.id, name="pilates")

        result = get_tags(db, sample_user.id)
        assert len(result) == 1
        assert result[0].name == "yoga"


class TestGetOrCreateTag:
    """Tests for get_or_create_tag."""

    def test_get_or_create_tag_new(self, db, sample_user):
        """get_or_create_tag creates a new tag when it doesn't exist."""
        data = TagInsert(user_id=sample_user.id, name="new-tag")
        result = get_or_create_tag(db, data)

        assert result.name == "new-tag"
        assert result.id is not None

    def test_get_or_create_tag_existing(self, db, sample_user):
        """get_or_create_tag returns existing tag with same id."""
        data = TagInsert(user_id=sample_user.id, name="existing")
        first = get_or_create_tag(db, data)
        second = get_or_create_tag(db, data)

        assert first.id == second.id


class TestDeleteTag:
    """Tests for delete_tag."""

    def test_delete_tag(self, db, sample_user, tag_factory):
        """Deleting an existing tag returns True."""
        tag = tag_factory(sample_user.id)
        assert delete_tag(db, tag.id) is True

    def test_delete_tag_not_found(self, db):
        """Deleting a nonexistent tag returns False."""
        assert delete_tag(db, uuid.uuid4()) is False
