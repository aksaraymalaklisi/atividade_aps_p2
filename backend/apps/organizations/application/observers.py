import logging
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class AuditEvent:
    def __init__(self, event_type: str, payload: dict[str, Any]):
        self.event_type = event_type
        self.payload = payload
        self.timestamp = datetime.now(UTC)


class AuditObserver(ABC):
    """
    Observer interface for Audit Logging.
    """

    @abstractmethod
    def update(self, event: AuditEvent) -> None:
        pass


class ConsoleAuditObserver(AuditObserver):
    """
    Simple observer that logs events to the console/logger.
    """

    def update(self, event: AuditEvent) -> None:
        logger.info(f"[AUDIT LOG] {event.timestamp.isoformat()} - {event.event_type}: {event.payload}")


class AuditSubject:
    """
    Subject that notifies observers of audit events.
    """

    def __init__(self):
        self._observers = []

    def attach(self, observer: AuditObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: AuditObserver) -> None:
        self._observers.remove(observer)

    def notify(self, event: AuditEvent) -> None:
        for observer in self._observers:
            observer.update(event)


# Global subject instance for application-wide use
audit_subject = AuditSubject()
audit_subject.attach(ConsoleAuditObserver())
