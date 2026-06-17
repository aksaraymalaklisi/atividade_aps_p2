import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from apps.chat.domain.entities import ChatRoom, ChatMessage


class ChatRoomRepositoryInterface(ABC):
    @abstractmethod
    def save(self, room: ChatRoom) -> ChatRoom:
        pass

    @abstractmethod
    def find_by_id(self, room_id: uuid.UUID) -> Optional[ChatRoom]:
        pass

    @abstractmethod
    def find_by_publication_and_interested_user(self, publication_id: uuid.UUID, interested_user_id: uuid.UUID) -> Optional[ChatRoom]:
        pass

    @abstractmethod
    def find_all_by_user(self, user_id: uuid.UUID) -> List[ChatRoom]:
        """Returns all chat rooms where the user is either the interested user or the publisher"""
        pass


class ChatMessageRepositoryInterface(ABC):
    @abstractmethod
    def save(self, message: ChatMessage) -> ChatMessage:
        pass

    @abstractmethod
    def find_by_id(self, message_id: uuid.UUID) -> Optional[ChatMessage]:
        pass

    @abstractmethod
    def find_by_room(self, room_id: uuid.UUID, limit: int = 50, offset: int = 0) -> Tuple[List[ChatMessage], int]:
        """Returns a tuple of (messages, total_count) ordered by sent_at ASC"""
        pass
        
    @abstractmethod
    def count_unread_for_user(self, user_id: uuid.UUID) -> int:
        """Returns total unread messages directed to the user across all rooms"""
        pass
        
    @abstractmethod
    def mark_all_as_read_for_user_in_room(self, room_id: uuid.UUID, user_id: uuid.UUID) -> int:
        """Marks all messages in a room as read, where the user is NOT the sender. Returns count updated."""
        pass
