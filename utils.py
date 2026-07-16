"""
=========================================================
Saad Python Project
utils.py
Version : 2.0
=========================================================
"""

from datetime import datetime
from typing import Any
import textwrap


def current_timestamp() -> str:
    """Return current date/time string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def separator(char: str = "-", length: int = 60) -> str:
    """Return a separator line."""
    return char * length


def truncate(text: str, max_length: int = 250) -> str:
    """Shorten long text for display."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def wrap_text(text: str, width: int = 100) -> str:
    """Wrap text to a fixed width."""
    return textwrap.fill(text, width=width)


def safe_get(data: dict, key: str, default: Any = None) -> Any:
    """Safely read a dictionary value."""
    return data.get(key, default)


def response_status_icon(status: str) -> str:
    """Return an icon for response status."""
    return {
        "success": "✅",
        "failed": "❌",
        "pending": "⏳",
    }.get(status.lower(), "❔")


def format_seconds(seconds: float) -> str:
    """Format elapsed time."""
    return f"{seconds:.2f} sec"


if __name__ == "__main__":
    print(separator("="))
    print("Saad Python Project - Utils Test")
    print(current_timestamp())
    print(truncate("This is a very long example string " * 10, 80))
    print(response_status_icon("success"))
    print(format_seconds(1.23456))
