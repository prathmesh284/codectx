# utils/__init__.py
"""Utility functions and helpers."""

from datetime import datetime
from zoneinfo import ZoneInfo


class TimestampUtils:
    """Timestamp utilities."""

    @staticmethod
    def get_ist_timestamp() -> str:
        """Get current time in Indian Standard Time (Mumbai)."""
        return datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()

    @staticmethod
    def get_utc_timestamp() -> str:
        """Get current time in UTC."""
        return datetime.utcnow().isoformat() + "Z"


class FormattingUtils:
    """Output formatting utilities."""

    @staticmethod
    def format_status(status: str, message: str) -> str:
        """Format status message."""
        return f"[{status}] {message}"

    @staticmethod
    def format_scan(message: str) -> str:
        return FormattingUtils.format_status("SCAN", message)

    @staticmethod
    def format_ok(message: str) -> str:
        return FormattingUtils.format_status("OK", message)

    @staticmethod
    def format_error(message: str) -> str:
        return FormattingUtils.format_status("ERROR", message)

    @staticmethod
    def format_info(message: str) -> str:
        return FormattingUtils.format_status("INFO", message)

    @staticmethod
    def format_plugin(message: str) -> str:
        return FormattingUtils.format_status("PLUGIN", message)

    @staticmethod
    def format_warn(message: str) -> str:
        return FormattingUtils.format_status("WARN", message)
