import uuid

from core.base_use_case import BaseUseCase
from apps.chat.domain.repositories import ChatMessageRepositoryInterface


class GetUnreadCountUseCase(BaseUseCase[uuid.UUID, int]):
    def __init__(self, chat_message_repository: ChatMessageRepositoryInterface):
        self.chat_message_repository = chat_message_repository

    def execute(self, user_id: uuid.UUID) -> int:
        return self.chat_message_repository.count_unread_for_user(user_id)
