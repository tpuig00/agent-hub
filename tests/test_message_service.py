import pytest

from app.domain.message import Channel, MessageStatus
from app.integrations.ai import AIResponder
from app.repositories.message_repository import InMemoryMessageRepository
from app.services.message_services import MessageService


class FakeAIResponder(AIResponder):
    """Sustituye a OpenAI en los tests: responde al instante, gratis y siempre lo mismo."""

    def __init__(self):
        self.calls = 0

    async def reply(self, text: str) -> str:
        self.calls += 1
        return f"Respuesta a: {text}"


def make_service() -> tuple[MessageService, InMemoryMessageRepository, FakeAIResponder]:
    repository = InMemoryMessageRepository()
    ai = FakeAIResponder()
    return MessageService(repository, ai), repository, ai


@pytest.mark.anyio
async def test_receive_answers_new_message():
    service, repository, _ = make_service()

    message = await service.receive("wamid.1", Channel.WHATSAPP, "+34600000000", "Hola")

    assert message.status == MessageStatus.ANSWERED
    assert message.reply == "Respuesta a: Hola"
    assert repository.get_by_id("wamid.1") == message


@pytest.mark.anyio
async def test_receive_same_id_twice_does_not_duplicate():
    service, _, _ = make_service()
    first = await service.receive("wamid.1", Channel.WHATSAPP, "+34600000000", "Hola")

    second = await service.receive("wamid.1", Channel.WHATSAPP, "+34600000000", "Otro texto")

    assert second is first
    assert second.content == "Hola"


@pytest.mark.anyio
async def test_receive_same_id_twice_calls_ai_only_once():
    service, _, ai = make_service()
    await service.receive("wamid.1", Channel.WHATSAPP, "+34600000000", "Hola")

    await service.receive("wamid.1", Channel.WHATSAPP, "+34600000000", "Hola")

    assert ai.calls == 1


def test_get_returns_none_when_message_does_not_exist():
    service, _, _ = make_service()

    assert service.get("no-existe") is None
