import pytest
import uuid
from datetime import datetime

from core.exceptions import ApplicationError
from apps.chat.domain.entities import ChatRoom, ChatMessage
from apps.chat.domain.value_objects import MessageType
from apps.chat.application.use_cases.start_chat import StartChatUseCase
from apps.chat.application.use_cases.send_message import SendMessageUseCase
from apps.chat.application.dtos import StartChatInput, SendMessageInput

class MockChatRoomRepository:
    def __init__(self):
        self.rooms = {}

    def save(self, room):
        self.rooms[room.id] = room
        return room

    def find_by_id(self, room_id):
        return self.rooms.get(room_id)

    def find_by_publication_and_interested_user(self, publication_id, interested_user_id):
        for room in self.rooms.values():
            if room.publication_id == publication_id and room.interested_user_id == interested_user_id:
                return room
        return None

    def find_all_by_user(self, user_id):
        return [r for r in self.rooms.values() if r.interested_user_id == user_id or r.publisher_user_id == user_id]


class MockChatMessageRepository:
    def __init__(self):
        self.messages = {}

    def save(self, message):
        self.messages[message.id] = message
        return message

    def find_by_id(self, message_id):
        return self.messages.get(message_id)

    def find_by_room(self, room_id, limit=50, offset=0):
        msgs = [m for m in self.messages.values() if m.chat_room_id == room_id]
        return msgs, len(msgs)

    def count_unread_for_user(self, user_id):
        return 0

    def mark_all_as_read_for_user_in_room(self, room_id, user_id):
        return 0


class MockPublicationRepository:
    def __init__(self):
        self.pubs = {}

    def save(self, pub):
        self.pubs[pub.id] = pub
        return pub

    def find_by_id(self, pub_id):
        return self.pubs.get(pub_id)


class MockPublication:
    def __init__(self, pub_id, publisher_id):
        self.id = pub_id
        self.publisher_id = publisher_id


@pytest.fixture
def repos():
    return {
        "chat_room": MockChatRoomRepository(),
        "chat_message": MockChatMessageRepository(),
        "publication": MockPublicationRepository(),
    }


def test_start_chat_success(repos):
    pub_id = uuid.uuid4()
    publisher_id = uuid.uuid4()
    interested_user_id = uuid.uuid4()
    
    repos["publication"].save(MockPublication(pub_id, publisher_id))
    
    use_case = StartChatUseCase(repos["chat_room"], repos["publication"])
    output = use_case.execute(StartChatInput(publication_id=pub_id, interested_user_id=interested_user_id))
    
    assert output.room_id is not None
    room = repos["chat_room"].find_by_id(output.room_id)
    assert room.publisher_user_id == publisher_id
    assert room.interested_user_id == interested_user_id


def test_start_chat_with_self_fails(repos):
    pub_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    repos["publication"].save(MockPublication(pub_id, user_id))
    
    use_case = StartChatUseCase(repos["chat_room"], repos["publication"])
    with pytest.raises(ApplicationError, match="Cannot start chat with yourself."):
        use_case.execute(StartChatInput(publication_id=pub_id, interested_user_id=user_id))


def test_send_message_success(repos):
    room_id = uuid.uuid4()
    publisher_id = uuid.uuid4()
    interested_user_id = uuid.uuid4()
    
    room = ChatRoom(
        id=room_id,
        publication_id=uuid.uuid4(),
        interested_user_id=interested_user_id,
        publisher_user_id=publisher_id
    )
    repos["chat_room"].save(room)
    
    use_case = SendMessageUseCase(repos["chat_room"], repos["chat_message"])
    output = use_case.execute(SendMessageInput(
        room_id=room_id,
        sender_id=interested_user_id,
        content="Hello!",
        message_type="TEXT"
    ))
    
    msg = repos["chat_message"].find_by_id(output.message_id)
    assert msg.content == "Hello!"
    assert msg.message_type == MessageType.TEXT


def test_send_address_share_by_non_publisher_fails(repos):
    room_id = uuid.uuid4()
    publisher_id = uuid.uuid4()
    interested_user_id = uuid.uuid4()
    
    room = ChatRoom(
        id=room_id,
        publication_id=uuid.uuid4(),
        interested_user_id=interested_user_id,
        publisher_user_id=publisher_id
    )
    repos["chat_room"].save(room)
    
    use_case = SendMessageUseCase(repos["chat_room"], repos["chat_message"])
    with pytest.raises(ApplicationError, match="Only the publisher can share the address."):
        use_case.execute(SendMessageInput(
            room_id=room_id,
            sender_id=interested_user_id,
            content="My address",
            message_type="ADDRESS_SHARE"
        ))
