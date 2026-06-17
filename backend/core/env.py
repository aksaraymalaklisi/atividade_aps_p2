"""
Environment variable validation utilities.

Provides helpers for loading env vars with clear error messages
when required variables are missing in production.
"""

import os
import sys


class MissingEnvVarError(Exception):
    """Raised when a required environment variable is not set."""


def require_env(name: str, description: str = "") -> str:
    """
    Get a required environment variable.

    Raises MissingEnvVarError with a descriptive message if the
    variable is not set. Used in production settings to fail fast.

    Args:
        name: The environment variable name.
        description: Human-readable description for error messages.

    Returns:
        The environment variable value.
    """
    value = os.getenv(name)
    if not value:
        desc = f" ({description})" if description else ""
        print(
            f"\n{'=' * 60}\n"
            f"  MISSING REQUIRED ENVIRONMENT VARIABLE\n"
            f"  Variable: {name}{desc}\n"
            f"  \n"
            f"  Please set this variable in your environment or .env file.\n"
            f"  See docs/deployment/environment.md for details.\n"
            f"{'=' * 60}\n",
            file=sys.stderr,
        )
        raise MissingEnvVarError(f"Required environment variable '{name}' is not set.{desc}")
    return value


def optional_env(name: str, default: str = "", description: str = "") -> str:
    """
    Get an optional environment variable with a default value.

    Args:
        name: The environment variable name.
        default: Default value if not set.
        description: Human-readable description (for documentation).

    Returns:
        The environment variable value or the default.
    """
    return os.getenv(name, default)
