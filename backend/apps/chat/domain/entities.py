import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from core.base_entity import BaseEntity
from apps.chat.domain.value_objects import MessageType


@dataclass
class ChatMessage(BaseEntity):
    chat_room_id: uuid.UUID | None = None
    sender_id: uuid.UUID | None = None
    content: str = ""
    message_type: MessageType = MessageType.TEXT
    is_read: bool = False
    sent_at: datetime = field(default_factory=datetime.now)

    def mark_as_read(self) -> None:
        self.is_read = True


@dataclass
class ChatRoom(BaseEntity):
    publication_id: uuid.UUID | None = None
    interested_user_id: uuid.UUID | None = None
    publisher_user_id: uuid.UUID | None = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def can_participate(self, user_id: uuid.UUID) -> bool:
        return user_id in [self.interested_user_id, self.publisher_user_id]
