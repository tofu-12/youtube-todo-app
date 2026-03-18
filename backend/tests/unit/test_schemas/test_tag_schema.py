"""Unit tests for Tag Pydantic schemas."""

import datetime
import uuid

import pytest
from pydantic import ValidationError

from app.crud.schemas.tag import TagInsert, TagResponse


class TestTagInsert:
    """Tests for TagInsert schema."""

    def test_tag_insert_valid(self):
        """TagInsert with user_id and name."""
        uid = uuid.uuid4()
        data = TagInsert(user_id=uid, name="yoga")
        assert data.user_id == uid
        assert data.name == "yoga"

    def test_tag_insert_missing_name(self):
        """TagInsert without name raises ValidationError."""
        with pytest.raises(ValidationError):
            TagInsert(user_id=uuid.uuid4())


class TestTagResponse:
    """Tests for TagResponse schema."""

    def test_tag_response_from_attributes(self):
        """TagResponse can be constructed from a dict."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        obj = {
            "id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "name": "yoga",
            "created_at": now,
            "updated_at": now,
        }
        result = TagResponse.model_validate(obj)
        assert result.name == "yoga"
