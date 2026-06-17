import uuid
from typing import Tuple

from core.base_use_case import BaseUseCase
from apps.chat.domain.repositories import ChatMessageRepositoryInterface, ChatRoomRepositoryInterface
from core.exceptions import ApplicationError


class MarkAsReadUseCase(BaseUseCase[Tuple[uuid.UUID, uuid.UUID], int]):
    def __init__(self, chat_room_repository: ChatRoomRepositoryInterface, chat_message_repository: ChatMessageRepositoryInterface):
        self.chat_room_repository = chat_room_repository
        self.chat_message_repository = chat_message_repository

    def execute(self, input_tuple: Tuple[uuid.UUID, uuid.UUID]) -> int:
        room_id, requesting_user_id = input_tuple
        
        room = self.chat_room_repository.find_by_id(room_id)
        if not room:
            raise ApplicationError("Chat room not found.", code="ROOM_NOT_FOUND")
            
        if not room.can_participate(requesting_user_id):
            raise ApplicationError("You cannot view messages in this room.", code="FORBIDDEN")
            
        updated_count = self.chat_message_repository.mark_all_as_read_for_user_in_room(room_id, requesting_user_id)
        return updated_count
