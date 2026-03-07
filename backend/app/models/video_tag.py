"""VideoTag model definition."""

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class VideoTag(TimestampMixin, Base):
    """Junction table for many-to-many relationship between Video and Tag."""

    __tablename__ = "video_tags"
    __table_args__ = (
        UniqueConstraint("video_id", "tag_id", name="uq_video_tag"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="video_tags")
    video = relationship("Video", back_populates="video_tags")
    tag = relationship("Tag", back_populates="video_tags")
