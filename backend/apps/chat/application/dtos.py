import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from apps.chat.domain.value_objects import MessageType


@dataclass
class StartChatInput:
    publication_id: uuid.UUID
    interested_user_id: uuid.UUID


@dataclass
class StartChatOutput:
    room_id: uuid.UUID


@dataclass
class SendMessageInput:
    room_id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    message_type: str  # "TEXT", "CONTACT_SHARE", "ADDRESS_SHARE"


@dataclass
class SendMessageOutput:
    message_id: uuid.UUID


@dataclass
class ChatMessageDTO:
    id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    message_type: str
    is_read: bool
    sent_at: datetime


@dataclass
class ChatRoomDTO:
    id: uuid.UUID
    publication_id: Optional[uuid.UUID]
    interested_user_id: Optional[uuid.UUID]
    publisher_user_id: Optional[uuid.UUID]
    created_at: datetime
    # Aggregated fields
    publication_title: str
    publication_image_url: Optional[str]
    other_user_id: Optional[uuid.UUID]
    other_user_name: str
    last_message: Optional[str]
    last_message_at: Optional[datetime]
    unread_count: int
