from typing import Optional


class AppError(Exception):
    """Base exception for application-specific errors."""

    status_code = 500
    default_detail = "An application error occurred."

    def __init__(self, detail: Optional[str] = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class InvalidInputError(AppError):
    status_code = 400
    default_detail = "Invalid input provided."


class LoadStateError(AppError):
    status_code = 500
    default_detail = "Failed to load tracker state."


class SaveStateError(AppError):
    status_code = 500
    default_detail = "Failed to save tracker state."
