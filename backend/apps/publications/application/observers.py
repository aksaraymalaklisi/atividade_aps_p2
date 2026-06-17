import logging
from typing import Any, Callable

from apps.publications.domain.entities import PublicationEntity

logger = logging.getLogger(__name__)


class PublicationEventPublisher:
    """
    Observer Pattern (Publisher)
    Notifies registered listeners when a new publication is created.
    """

    def __init__(self):
        self._listeners: list[Callable[[PublicationEntity], Any]] = []

    def subscribe(self, listener: Callable[[PublicationEntity], Any]) -> None:
        self._listeners.append(listener)

    def notify_created(self, publication: PublicationEntity) -> None:
        for listener in self._listeners:
            try:
                listener(publication)
            except Exception as e:
                # We catch exceptions so one failing listener doesn't break others or the main transaction
                logger.error(f"Error notifying listener {listener}: {e}")


# Pre-configured global publisher for simplicity in this MVP
publication_event_publisher = PublicationEventPublisher()


# Sample listener (Observer)
def log_publication_creation(publication: PublicationEntity) -> None:
    logger.info(f"New publication created! ID: {publication.id}, Status: {publication.status}")

publication_event_publisher.subscribe(log_publication_creation)
