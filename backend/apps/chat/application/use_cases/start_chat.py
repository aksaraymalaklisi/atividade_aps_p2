import uuid

from core.base_use_case import BaseUseCase
from apps.chat.application.dtos import StartChatInput, StartChatOutput
from apps.chat.domain.entities import ChatRoom
from apps.chat.domain.repositories import ChatRoomRepositoryInterface
from apps.publications.domain.repositories import PublicationRepositoryInterface
from core.exceptions import ApplicationError


class StartChatUseCase(BaseUseCase[StartChatInput, StartChatOutput]):
    def __init__(self, chat_room_repository: ChatRoomRepositoryInterface, publication_repository: PublicationRepositoryInterface):
        self.chat_room_repository = chat_room_repository
        self.publication_repository = publication_repository

    def execute(self, input_dto: StartChatInput) -> StartChatOutput:
        # Check if publication exists
        publication = self.publication_repository.get_by_id(input_dto.publication_id)
        if not publication:
            raise ApplicationError("Publication not found.")
            
        # Check if chat already exists for this pair
        existing_room = self.chat_room_repository.find_by_publication_and_interested_user(
            publication_id=input_dto.publication_id,
            interested_user_id=input_dto.interested_user_id
        )
        
        if existing_room:
            return StartChatOutput(room_id=existing_room.id)
            
        # Cannot start chat with oneself
        if publication.publisher_id == input_dto.interested_user_id:
            raise ApplicationError("Cannot start chat with yourself.")
            
        # Create new room
        new_room = ChatRoom(
            id=uuid.uuid4(),
            publication_id=publication.id,
            interested_user_id=input_dto.interested_user_id,
            publisher_user_id=publication.publisher_id
        )
        
        saved_room = self.chat_room_repository.save(new_room)
        return StartChatOutput(room_id=saved_room.id)
