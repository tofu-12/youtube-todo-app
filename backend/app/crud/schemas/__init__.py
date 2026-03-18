"""CRUD schema definitions."""

from app.crud.schemas.recurrence import (
    RecurrenceResponse,
    RecurrenceUpsert,
    WeekdayResponse,
)
from app.crud.schemas.tag import TagInsert, TagResponse
from app.crud.schemas.todo_history import (
    TodoHistoryFilter,
    TodoHistoryInsert,
    TodoHistoryResponse,
)
from app.crud.schemas.user import UserInsert, UserResponse, UserUpdate
from app.crud.schemas.video import (
    VideoFilter,
    VideoInsert,
    VideoResponse,
    VideoUpdate,
)
from app.crud.schemas.workout_history import (
    WorkoutHistoryFilter,
    WorkoutHistoryInsert,
    WorkoutHistoryResponse,
)

__all__ = [
    "RecurrenceResponse",
    "RecurrenceUpsert",
    "TagInsert",
    "TagResponse",
    "TodoHistoryFilter",
    "TodoHistoryInsert",
    "TodoHistoryResponse",
    "UserInsert",
    "UserResponse",
    "UserUpdate",
    "VideoFilter",
    "VideoInsert",
    "VideoResponse",
    "VideoUpdate",
    "WeekdayResponse",
    "WorkoutHistoryFilter",
    "WorkoutHistoryInsert",
    "WorkoutHistoryResponse",
]
