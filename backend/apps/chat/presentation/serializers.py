from rest_framework import serializers

class StartChatInputSerializer(serializers.Serializer):
    publication_id = serializers.UUIDField()

class SendMessageInputSerializer(serializers.Serializer):
    content = serializers.CharField(allow_blank=True, max_length=5000)
    message_type = serializers.ChoiceField(choices=["TEXT", "CONTACT_SHARE", "ADDRESS_SHARE"], default="TEXT")

class ChatRoomOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    publication_id = serializers.UUIDField()
    interested_user_id = serializers.UUIDField()
    publisher_user_id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    publication_title = serializers.CharField()
    publication_image_url = serializers.CharField(allow_null=True)
    other_user_id = serializers.UUIDField()
    other_user_name = serializers.CharField()
    last_message = serializers.CharField(allow_null=True)
    last_message_at = serializers.DateTimeField(allow_null=True)
    unread_count = serializers.IntegerField()

class ChatMessageOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    sender_id = serializers.UUIDField()
    content = serializers.CharField()
    message_type = serializers.CharField()
    is_read = serializers.BooleanField()
    sent_at = serializers.DateTimeField()
