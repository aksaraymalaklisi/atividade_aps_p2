import uuid
from typing import List, Optional, Tuple
from django.db.models import Q

from apps.chat.domain.entities import ChatRoom, ChatMessage
from apps.chat.domain.value_objects import MessageType
from apps.chat.domain.repositories import ChatRoomRepositoryInterface, ChatMessageRepositoryInterface
from apps.chat.models import ChatRoom as ChatRoomModel, ChatMessage as ChatMessageModel


class DjangoChatRoomRepository(ChatRoomRepositoryInterface):
    def _to_entity(self, model: ChatRoomModel) -> ChatRoom:
        return ChatRoom(
            id=model.id,
            publication_id=model.publication_id,
            interested_user_id=model.interested_user_id,
            publisher_user_id=model.publisher_user_id,
            created_at=model.created_at
        )

    def save(self, room: ChatRoom) -> ChatRoom:
        model, created = ChatRoomModel.objects.update_or_create(
            id=room.id,
            defaults={
                "publication_id": room.publication_id,
                "interested_user_id": room.interested_user_id,
                "publisher_user_id": room.publisher_user_id,
                "created_at": room.created_at
            }
        )
        return self._to_entity(model)

    def find_by_id(self, room_id: uuid.UUID) -> Optional[ChatRoom]:
        try:
            model = ChatRoomModel.objects.get(id=room_id)
            return self._to_entity(model)
        except ChatRoomModel.DoesNotExist:
            return None

    def find_by_publication_and_interested_user(self, publication_id: uuid.UUID, interested_user_id: uuid.UUID) -> Optional[ChatRoom]:
        try:
            model = ChatRoomModel.objects.get(publication_id=publication_id, interested_user_id=interested_user_id)
            return self._to_entity(model)
        except ChatRoomModel.DoesNotExist:
            return None

    def find_all_by_user(self, user_id: uuid.UUID) -> List[ChatRoom]:
        models = ChatRoomModel.objects.filter(
            Q(interested_user_id=user_id) | Q(publisher_user_id=user_id)
        ).select_related("publication", "interested_user", "publisher_user").order_by("-created_at")
        return [self._to_entity(m) for m in models]


class DjangoChatMessageRepository(ChatMessageRepositoryInterface):
    def _to_entity(self, model: ChatMessageModel) -> ChatMessage:
        return ChatMessage(
            id=model.id,
            chat_room_id=model.chat_room_id,
            sender_id=model.sender_id,
            content=model.content,
            message_type=MessageType(model.message_type),
            is_read=model.is_read,
            sent_at=model.sent_at
        )

    def save(self, message: ChatMessage) -> ChatMessage:
        model, created = ChatMessageModel.objects.update_or_create(
            id=message.id,
            defaults={
                "chat_room_id": message.chat_room_id,
                "sender_id": message.sender_id,
                "content": message.content,
                "message_type": message.message_type.value,
                "is_read": message.is_read,
                "sent_at": message.sent_at
            }
        )
        return self._to_entity(model)

    def find_by_id(self, message_id: uuid.UUID) -> Optional[ChatMessage]:
        try:
            model = ChatMessageModel.objects.get(id=message_id)
            return self._to_entity(model)
        except ChatMessageModel.DoesNotExist:
            return None

    def find_by_room(self, room_id: uuid.UUID, limit: int = 50, offset: int = 0) -> Tuple[List[ChatMessage], int]:
        queryset = ChatMessageModel.objects.filter(chat_room_id=room_id).order_by("-sent_at")
        total_count = queryset.count()
        models = list(queryset[offset:offset+limit])
        # Reverse to get chronological order for chat view
        models.reverse()
        return [self._to_entity(m) for m in models], total_count

    def count_unread_for_user(self, user_id: uuid.UUID) -> int:
        return ChatMessageModel.objects.filter(
            chat_room__interested_user_id=user_id
        ).filter(
            ~Q(sender_id=user_id),
            is_read=False
        ).count() + ChatMessageModel.objects.filter(
            chat_room__publisher_user_id=user_id
        ).filter(
            ~Q(sender_id=user_id),
            is_read=False
        ).count()

    def mark_all_as_read_for_user_in_room(self, room_id: uuid.UUID, user_id: uuid.UUID) -> int:
        return ChatMessageModel.objects.filter(
            chat_room_id=room_id,
            is_read=False
        ).exclude(
            sender_id=user_id
        ).update(is_read=True)
