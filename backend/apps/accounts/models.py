"""
Accounts models — re-export from infrastructure layer.

Django requires models to be discoverable at the app level (apps.accounts.models).
The actual model definitions live in the infrastructure layer, following Clean Architecture.
This file bridges the gap by re-exporting them.
"""

from apps.accounts.infrastructure.models import User

__all__ = ["User"]
