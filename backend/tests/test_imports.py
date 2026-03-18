"""Import tests to verify all modules can be imported without errors."""

import importlib

import pytest


# -- Module import tests (parameterized) ------------------------------------

MODULE_PATHS = [
    # Core
    "app.core.types",
    "app.core.database",
    "app.core.dependencies",
    # Config
    "app.config",
    # Models
    "app.models",
    "app.models.base",
    "app.models.user",
    "app.models.video",
    "app.models.tag",
    "app.models.video_tag",
    "app.models.video_recurrence",
    "app.models.video_weekday",
    "app.models.todo_history",
    "app.models.workout_history",
    # API
    "app.api",
    "app.api.videos",
    "app.api.today",
    "app.api.settings",
    "app.api.recurrences",
    "app.api.todo_histories",
    "app.api.workout_histories",
    "app.api.schemas",
    "app.api.schemas.video",
    # CRUD
    "app.crud",
    "app.crud.video",
    "app.crud.recurrence",
    "app.crud.schemas",
    "app.crud.schemas.video",
    # Services
    "app.services",
    "app.services.video_service",
    "app.services.settings_service",
    "app.services.recurrence_service",
    # Main
    "app.main",
]


@pytest.mark.parametrize("module_path", MODULE_PATHS)
def test_import_module(module_path: str) -> None:
    """Verify that each module can be imported without raising an error."""
    module = importlib.import_module(module_path)
    assert module is not None


# -- Attribute existence tests ----------------------------------------------

ATTRIBUTE_CASES = [
    ("app.core.types", ["RecurrenceType", "DayOfWeek", "TodoStatus"]),
    ("app.core.database", ["Base", "engine", "SessionLocal"]),
    ("app.core.dependencies", ["get_db"]),
    ("app.config", ["AppSettings", "DevSettings", "TestSettings", "settings"]),
    (
        "app.models",
        [
            "Base",
            "User",
            "Video",
            "Tag",
            "VideoTag",
            "VideoRecurrence",
            "VideoWeekday",
            "TodoHistory",
            "WorkoutHistory",
            "RecurrenceType",
            "DayOfWeek",
            "TodoStatus",
        ],
    ),
    ("app.main", ["app"]),
]


@pytest.mark.parametrize(
    ("module_path", "attributes"),
    ATTRIBUTE_CASES,
    ids=[case[0] for case in ATTRIBUTE_CASES],
)
def test_module_exports(module_path: str, attributes: list[str]) -> None:
    """Verify that key public attributes are accessible after import."""
    module = importlib.import_module(module_path)
    for attr in attributes:
        assert hasattr(module, attr), (
            f"{module_path} is missing expected attribute '{attr}'"
        )
