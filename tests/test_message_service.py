from datetime import timedelta

import pytest

from app.domain.conversation import Channel, ConversationStatus
from app.domain.message import Direction
from app.integrations.ai import AIResponder
from app.repositories.conversation_repository import InMemoryConversationRepository
from app.repositories.message_repository import InMemoryMessageRepository
from app.services.message_services import MessageService

CUSTOMER = "ES.13491208655302741918"
TIMEOUT = timedelta(hours=2)


class FakeAIResponder(AIResponder):
    """Sustituye a OpenAI en los tests: responde al instante, gratis y siempre lo mismo."""

    def __init__(self):
        self.started = 0
        self.replies = 0

    async def start_conversation(self) -> str:
        self.started += 1
        return f"conv_{self.started}"

    async def reply(self, ai_conversation_id: str, text: str) -> str:
        self.replies += 1
        return f"Respuesta a: {text}"


def make_service():
    messages = InMemoryMessageRepository()
    conversations = InMemoryConversationRepository()
    ai = FakeAIResponder()
    return MessageService(messages, conversations, ai, TIMEOUT), messages, conversations, ai


@pytest.mark.anyio
async def test_receive_saves_inbound_and_reply_in_the_same_conversation():
    service, messages, _, _ = make_service()

    reply = await service.receive("wamid.1", Channel.WHATSAPP, CUSTOMER, "Hola")

    inbound = messages.get_by_external_id("wamid.1")
    assert reply.direction == Direction.OUTBOUND
    assert reply.content == "Respuesta a: Hola"
    assert inbound.conversation_id == reply.conversation_id
    assert messages.get_by_id(reply.id) == reply


@pytest.mark.anyio
async def test_receive_same_external_id_twice_is_ignored():
    service, _, _, ai = make_service()
    await service.receive("wamid.1", Channel.WHATSAPP, CUSTOMER, "Hola")

    second = await service.receive("wamid.1", Channel.WHATSAPP, CUSTOMER, "Hola")

    assert second is None
    assert ai.replies == 1


@pytest.mark.anyio
async def test_messages_from_same_customer_share_the_open_conversation():
    service, _, _, ai = make_service()

    first = await service.receive("wamid.1", Channel.WHATSAPP, CUSTOMER, "Hola")
    second = await service.receive("wamid.2", Channel.WHATSAPP, CUSTOMER, "¿Abrís el sábado?")

    assert first.conversation_id == second.conversation_id
    assert ai.started == 1


@pytest.mark.anyio
async def test_expired_conversation_is_closed_and_a_new_one_starts():
    service, _, conversations, ai = make_service()
    first = await service.receive("wamid.1", Channel.WHATSAPP, CUSTOMER, "Hola")
    old = conversations.get_open(Channel.WHATSAPP, CUSTOMER)
    # Simulamos que han pasado más de 2 horas desde el último mensaje
    old.last_activity_at -= TIMEOUT + timedelta(minutes=1)

    second = await service.receive("wamid.2", Channel.WHATSAPP, CUSTOMER, "Hola de nuevo")

    assert second.conversation_id != first.conversation_id
    assert old.status == ConversationStatus.CLOSED
    assert ai.started == 2


def test_get_returns_none_when_message_does_not_exist():
    service, _, _, _ = make_service()

    assert service.get("no-existe") is None
