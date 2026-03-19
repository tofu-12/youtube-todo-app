"""API schemas for authentication endpoints."""

import uuid

from pydantic import BaseModel, field_validator


class AuthRequest(BaseModel):
    """Request body for login or registration."""

    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Check that the email contains an @ sign."""
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.strip().lower()


class AuthResponse(BaseModel):
    """Response body after successful authentication."""

    id: uuid.UUID
    email: str
