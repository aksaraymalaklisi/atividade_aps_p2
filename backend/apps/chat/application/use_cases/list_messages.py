import uuid
from typing import List, Tuple

from core.base_use_case import BaseUseCase
from apps.chat.application.dtos import ChatMessageDTO
from apps.chat.domain.repositories import ChatMessageRepositoryInterface, ChatRoomRepositoryInterface
from core.exceptions import ApplicationError


class ListMessagesUseCase(BaseUseCase[Tuple[uuid.UUID, uuid.UUID], List[ChatMessageDTO]]):
    def __init__(self, chat_room_repository: ChatRoomRepositoryInterface, chat_message_repository: ChatMessageRepositoryInterface):
        self.chat_room_repository = chat_room_repository
        self.chat_message_repository = chat_message_repository

    def execute(self, input_tuple: Tuple[uuid.UUID, uuid.UUID]) -> List[ChatMessageDTO]:
        room_id, requesting_user_id = input_tuple
        
        room = self.chat_room_repository.find_by_id(room_id)
        if not room:
            raise ApplicationError("Chat room not found.", code="ROOM_NOT_FOUND")
            
        if not room.can_participate(requesting_user_id):
            raise ApplicationError("You cannot view messages in this room.", code="FORBIDDEN")
            
        messages, _ = self.chat_message_repository.find_by_room(room_id, limit=200) # Simple limit for MVP
        
        dtos = [
            ChatMessageDTO(
                id=m.id,
                sender_id=m.sender_id,
                content=m.content,
                message_type=m.message_type.value,
                is_read=m.is_read,
                sent_at=m.sent_at
            ) for m in messages
        ]
        
        return dtos
