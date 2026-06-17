"""
Base use case class for the application layer.

Use cases orchestrate the flow of data between the presentation layer
and the domain layer. Each use case represents a single application
action (Single Responsibility Principle).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


@dataclass
class UseCaseInput:
    """Base class for use case input DTOs."""


@dataclass
class UseCaseOutput:
    """Base class for use case output DTOs."""


class BaseUseCase[InputDTO, OutputDTO](ABC):
    """
    Abstract base class for all use cases.

    Each use case implements a single `execute` method that takes
    an input DTO and returns an output DTO. This ensures a consistent
    interface across all application actions.
    """

    @abstractmethod
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """Execute the use case with the given input."""
