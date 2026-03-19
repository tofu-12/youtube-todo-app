"""Shared validation utilities."""

import re


YOUTUBE_URL_PATTERN = re.compile(
    r"^https?://(www\.|m\.)?(youtube\.com|youtu\.be)/.+"
)


def validate_youtube_url(url: str) -> str:
    """Validate that the given URL is a YouTube URL.

    Args:
        url: The URL string to validate.

    Returns:
        The validated URL string.

    Raises:
        ValueError: If the URL is not a valid YouTube URL.
    """
    if not YOUTUBE_URL_PATTERN.match(url):
        raise ValueError(
            "URL must be a valid YouTube URL "
            "(e.g. https://www.youtube.com/watch?v=... or https://youtu.be/...)"
        )
    return url
