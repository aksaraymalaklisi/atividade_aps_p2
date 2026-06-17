from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.chat.presentation.serializers import (
    StartChatInputSerializer, 
    SendMessageInputSerializer, 
    ChatRoomOutputSerializer,
    ChatMessageOutputSerializer
)
from apps.chat.application.use_cases.start_chat import StartChatUseCase
from apps.chat.application.use_cases.list_chats import ListChatsUseCase
from apps.chat.application.use_cases.send_message import SendMessageUseCase
from apps.chat.application.use_cases.list_messages import ListMessagesUseCase
from apps.chat.application.use_cases.mark_as_read import MarkAsReadUseCase
from apps.chat.application.use_cases.get_unread_count import GetUnreadCountUseCase
from apps.chat.application.dtos import StartChatInput, SendMessageInput
from apps.chat.infrastructure.repositories import DjangoChatRoomRepository, DjangoChatMessageRepository
from apps.publications.infrastructure.repositories import DjangoPublicationRepository
from core.exceptions import ApplicationError


class ChatViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        use_case = ListChatsUseCase(DjangoChatRoomRepository(), DjangoPublicationRepository())
        dtos = use_case.execute(request.user.id)
        serializer = ChatRoomOutputSerializer(dtos, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StartChatInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = StartChatUseCase(DjangoChatRoomRepository(), DjangoPublicationRepository())
        try:
            output = use_case.execute(StartChatInput(
                publication_id=serializer.validated_data["publication_id"],
                interested_user_id=request.user.id
            ))
            return Response({"room_id": output.room_id}, status=status.HTTP_201_CREATED)
        except ApplicationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        use_case = GetUnreadCountUseCase(DjangoChatMessageRepository())
        count = use_case.execute(request.user.id)
        return Response({"unread_count": count})

    @action(detail=True, methods=["get"], url_path="messages")
    def list_messages(self, request, pk=None):
        use_case = ListMessagesUseCase(DjangoChatRoomRepository(), DjangoChatMessageRepository())
        try:
            dtos = use_case.execute((pk, request.user.id))
            serializer = ChatMessageOutputSerializer(dtos, many=True)
            return Response(serializer.data)
        except ApplicationError as e:
            # Map code FORBIDDEN to 403
            status_code = status.HTTP_403_FORBIDDEN if hasattr(e, "code") and e.code == "FORBIDDEN" else status.HTTP_400_BAD_REQUEST
            if hasattr(e, "code") and e.code == "ROOM_NOT_FOUND":
                status_code = status.HTTP_404_NOT_FOUND
            return Response({"error": str(e)}, status=status_code)

    @action(detail=True, methods=["post"], url_path="messages/send")
    def send_message(self, request, pk=None):
        serializer = SendMessageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = SendMessageUseCase(DjangoChatRoomRepository(), DjangoChatMessageRepository())
        try:
            output = use_case.execute(SendMessageInput(
                room_id=pk,
                sender_id=request.user.id,
                content=serializer.validated_data["content"],
                message_type=serializer.validated_data["message_type"]
            ))
            return Response({"message_id": output.message_id}, status=status.HTTP_201_CREATED)
        except ApplicationError as e:
            status_code = status.HTTP_403_FORBIDDEN if hasattr(e, "code") and e.code == "FORBIDDEN" else status.HTTP_400_BAD_REQUEST
            if hasattr(e, "code") and e.code == "ROOM_NOT_FOUND":
                status_code = status.HTTP_404_NOT_FOUND
            return Response({"error": str(e)}, status=status_code)

    @action(detail=True, methods=["post"], url_path="messages/read")
    def mark_as_read(self, request, pk=None):
        use_case = MarkAsReadUseCase(DjangoChatRoomRepository(), DjangoChatMessageRepository())
        try:
            updated_count = use_case.execute((pk, request.user.id))
            return Response({"updated_count": updated_count}, status=status.HTTP_200_OK)
        except ApplicationError as e:
            status_code = status.HTTP_403_FORBIDDEN if hasattr(e, "code") and e.code == "FORBIDDEN" else status.HTTP_400_BAD_REQUEST
            if hasattr(e, "code") and e.code == "ROOM_NOT_FOUND":
                status_code = status.HTTP_404_NOT_FOUND
            return Response({"error": str(e)}, status=status_code)
