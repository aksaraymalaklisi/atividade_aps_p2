import uuid
from django.db import models
from django.conf import settings

from apps.publications.models import Publication
from apps.chat.domain.value_objects import MessageType


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="chat_rooms")
    interested_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interested_chats")
    publisher_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="publisher_chats")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_rooms"
        unique_together = ("publication", "interested_user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Chat {self.id} (Pub: {self.publication.id})"


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    
    MESSAGE_TYPE_CHOICES = [(tag.value, tag.value) for tag in MessageType]
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default=MessageType.TEXT.value)
    
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_messages"
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message {self.id} by {self.sender.email}"
