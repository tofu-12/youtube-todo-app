"""Pydantic schemas for Tag CRUD operations."""

import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class TagInsert(BaseModel):
    """Schema for creating a new tag."""

    user_id: uuid.UUID
    name: str


class TagResponse(BaseModel):
    """Schema for returning tag data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
