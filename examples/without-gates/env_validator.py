"""Environment variable validator with type checking and defaults."""
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class ValidationResult:
    """Result of environment validation."""
    valid: bool
    missing: list[str]
    present: list[str]
    errors: list[str]

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "missing": self.missing,
            "present": self.present,
            "errors": self.errors
        }


class EnvValidator:
    """Validates environment variables with type checking and defaults."""

    def __init__(self):
        self.required: list[str] = []
        self.defaults: dict[str, Any] = {}
        self.type_validators: dict[str, Callable] = {}

    def add_required(self, name: str) -> "EnvValidator":
        """Add a required environment variable."""
        self.required.append(name)
        return self

    def add_default(self, name: str, value: Any) -> "EnvValidator":
        """Add a default value for an environment variable."""
        self.defaults[name] = value
        return self

    def add_type_validator(self, name: str, validator: Callable) -> "EnvValidator":
        """Add a type validator for an environment variable."""
        self.type_validators[name] = validator
        return self

    def validate(self) -> ValidationResult:
        """Validate all environment variables."""
        missing = []
        present = []
        errors = []

        for var in self.required:
            value = os.environ.get(var)
            if value is None:
                if var in self.defaults:
                    os.environ[var] = str(self.defaults[var])
                    present.append(var)
                else:
                    missing.append(var)
            else:
                present.append(var)
                if var in self.type_validators:
                    try:
                        self.type_validators[var](value)
                    except Exception as e:
                        errors.append(f"{var}: {e}")

        return ValidationResult(
            valid=len(missing) == 0 and len(errors) == 0,
            missing=missing,
            present=present,
            errors=errors
        )
