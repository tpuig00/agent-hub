import pytest

from app.domain.message import Channel, Message, MessageStatus


def make_message() -> Message:
    return Message(id="wamid.1", channel=Channel.WHATSAPP, sender="+34600000000", content="Hola")


def test_mark_as_answered_saves_reply_and_changes_status():
    message = make_message()

    message.mark_as_answered("¡Hola! ¿En qué te ayudo?")

    assert message.status == MessageStatus.ANSWERED
    assert message.reply == "¡Hola! ¿En qué te ayudo?"


def test_mark_as_answered_twice_raises_error():
    message = make_message()
    message.mark_as_answered("Primera respuesta")

    with pytest.raises(ValueError):
        message.mark_as_answered("Segunda respuesta")

    # La regla no solo lanza el error: también protege la respuesta que ya había
    assert message.reply == "Primera respuesta"
