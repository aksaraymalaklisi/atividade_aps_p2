import uuid
from typing import Optional

from core.base_use_case import BaseUseCase
from apps.chat.application.dtos import SendMessageInput, SendMessageOutput
from apps.chat.domain.entities import ChatMessage
from apps.chat.domain.value_objects import MessageType
from apps.chat.domain.repositories import ChatRoomRepositoryInterface, ChatMessageRepositoryInterface
from core.exceptions import ApplicationError


class SendMessageUseCase(BaseUseCase[SendMessageInput, SendMessageOutput]):
    def __init__(self, chat_room_repository: ChatRoomRepositoryInterface, chat_message_repository: ChatMessageRepositoryInterface):
        self.chat_room_repository = chat_room_repository
        self.chat_message_repository = chat_message_repository

    def execute(self, input_dto: SendMessageInput) -> SendMessageOutput:
        room = self.chat_room_repository.find_by_id(input_dto.room_id)
        if not room:
            raise ApplicationError("Chat room not found.", code="ROOM_NOT_FOUND")
            
        if not room.can_participate(input_dto.sender_id):
            raise ApplicationError("You cannot send messages to this room.", code="FORBIDDEN")
            
        try:
            msg_type = MessageType(input_dto.message_type)
        except ValueError:
            raise ApplicationError(f"Invalid message type: {input_dto.message_type}")
            
        # Business rule: only publisher can send ADDRESS_SHARE
        if msg_type == MessageType.ADDRESS_SHARE and input_dto.sender_id != room.publisher_user_id:
            raise ApplicationError("Only the publisher can share the address.", code="FORBIDDEN")

        message = ChatMessage(
            id=uuid.uuid4(),
            chat_room_id=room.id,
            sender_id=input_dto.sender_id,
            content=input_dto.content,
            message_type=msg_type
        )
        
        saved_message = self.chat_message_repository.save(message)
        return SendMessageOutput(message_id=saved_message.id)
