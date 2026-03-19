"""CRUD operations for Tag model."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.schemas.tag import TagInsert, TagResponse
from app.models.tag import Tag


def create_tag(db: Session, data: TagInsert) -> TagResponse:
    """Create a new tag."""
    tag = Tag(**data.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return TagResponse.model_validate(tag)


def get_tags(db: Session, user_id: uuid.UUID) -> list[TagResponse]:
    """Get all tags for a user."""
    stmt = select(Tag).where(Tag.user_id == user_id)
    tags = db.scalars(stmt).all()
    return [TagResponse.model_validate(t) for t in tags]


def get_or_create_tag(db: Session, data: TagInsert) -> TagResponse:
    """Get an existing tag by name or create a new one."""
    stmt = select(Tag).where(
        Tag.user_id == data.user_id, Tag.name == data.name
    )
    tag = db.scalars(stmt).first()
    if tag is not None:
        return TagResponse.model_validate(tag)
    return create_tag(db, data)


def get_or_create_tags_bulk(
    db: Session, user_id: uuid.UUID, names: list[str]
) -> list[TagResponse]:
    """Get or create multiple tags by name in bulk."""
    if not names:
        return []
    unique_names = list(dict.fromkeys(names))
    stmt = select(Tag).where(Tag.user_id == user_id, Tag.name.in_(unique_names))
    existing = {t.name: t for t in db.scalars(stmt).all()}
    result = []
    for name in unique_names:
        if name in existing:
            result.append(TagResponse.model_validate(existing[name]))
        else:
            tag = Tag(user_id=user_id, name=name)
            db.add(tag)
            db.flush()
            existing[name] = tag
            result.append(TagResponse.model_validate(tag))
    return result


def delete_tag(db: Session, tag_id: uuid.UUID) -> bool:
    """Delete a tag. Returns True if deleted, False if not found."""
    tag = db.get(Tag, tag_id)
    if tag is None:
        return False
    db.delete(tag)
    db.commit()
    return True
