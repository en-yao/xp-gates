import os


def validate_env(required: list[str]) -> list[str]:
    """Return names of missing environment variables."""
    return [var for var in required if var not in os.environ]
