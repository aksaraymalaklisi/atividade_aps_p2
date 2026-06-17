import uuid
from typing import List

from core.base_use_case import BaseUseCase
from apps.chat.application.dtos import ChatRoomDTO
from apps.chat.domain.repositories import ChatRoomRepositoryInterface
from apps.publications.domain.repositories import PublicationRepositoryInterface
from django.contrib.auth import get_user_model
from apps.chat.models import ChatMessage as ChatMessageModel


User = get_user_model()


class ListChatsUseCase(BaseUseCase[uuid.UUID, List[ChatRoomDTO]]):
    def __init__(self, chat_room_repository: ChatRoomRepositoryInterface, publication_repository: PublicationRepositoryInterface):
        self.chat_room_repository = chat_room_repository
        self.publication_repository = publication_repository

    def execute(self, user_id: uuid.UUID) -> List[ChatRoomDTO]:
        rooms = self.chat_room_repository.find_all_by_user(user_id)
        dtos = []
        
        for room in rooms:
            # We violate strict boundaries slightly for rapid data fetching of the User model 
            # (which is in Django contrib auth) to avoid duplicating a UserRepository here just for names.
            # In a strict CQRS architecture, this would be a specialized ReadModel Query.
            
            is_publisher = (room.publisher_user_id == user_id)
            other_user_id = room.interested_user_id if is_publisher else room.publisher_user_id
            
            try:
                other_user = User.objects.get(id=other_user_id)
                other_user_name = getattr(other_user, 'first_name', '') or getattr(other_user, 'username', 'Unknown User')
            except User.DoesNotExist:
                other_user_name = "Unknown User"
                
            if not room.publication_id:
                continue
                
            publication = self.publication_repository.get_by_id(room.publication_id)
            if not publication:
                continue
                
            # Fetch last message and unread count via ORM for performance
            # In pure CA this would be a method on ChatMessageRepositoryInterface
            last_msg = ChatMessageModel.objects.filter(chat_room_id=room.id).order_by('-sent_at').first()
            
            unread_count = ChatMessageModel.objects.filter(
                chat_room_id=room.id,
                is_read=False
            ).exclude(sender_id=user_id).count()
            
            # primary image
            primary_image = None
            if publication.pet and publication.pet.images:
                primary_image = next((img.image for img in publication.pet.images if img.is_primary), None)
                if not primary_image:
                    primary_image = publication.pet.images[0].image
                    
            pub_title = publication.pet.name if publication.pet else "Sem Título"
                
            dtos.append(ChatRoomDTO(
                id=room.id,
                publication_id=room.publication_id,
                interested_user_id=room.interested_user_id,
                publisher_user_id=room.publisher_user_id,
                created_at=room.created_at,
                publication_title=pub_title,
                publication_image_url=primary_image,
                other_user_id=other_user_id,
                other_user_name=other_user_name,
                last_message=last_msg.content if last_msg else None,
                last_message_at=last_msg.sent_at if last_msg else None,
                unread_count=unread_count
            ))
            
        # Sort by last message time, fallback to created_at
        dtos.sort(key=lambda x: x.last_message_at or x.created_at, reverse=True)
        return dtos
