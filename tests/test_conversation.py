from datetime import UTC, datetime, timedelta

import pytest

from app.domain.conversation import Conversation, ConversationStatus
from app.domain.message import Channel

START = datetime(2026, 10, 27, 12, 0, tzinfo=UTC)
TIMEOUT = timedelta(hours=2)


def make_conversation() -> Conversation:
    return Conversation(
        id="conv-1",
        channel=Channel.WHATSAPP,
        customer_id="ES.13491208655302741918",
        ai_conversation_id="conv_abc",
        last_activity_at=START,
    )


def test_new_conversation_is_open():
    assert make_conversation().status == ConversationStatus.OPEN


def test_is_not_expired_within_timeout():
    conversation = make_conversation()

    assert not conversation.is_expired(START + TIMEOUT, TIMEOUT)


def test_is_expired_after_timeout():
    conversation = make_conversation()

    assert conversation.is_expired(START + TIMEOUT + timedelta(seconds=1), TIMEOUT)


def test_register_activity_extends_the_conversation():
    conversation = make_conversation()

    conversation.register_activity(START + timedelta(hours=1))

    # Sin la actividad nueva, a las 2h 30min ya habría caducado
    assert not conversation.is_expired(START + timedelta(hours=2, minutes=30), TIMEOUT)


def test_register_activity_on_closed_conversation_raises_error():
    conversation = make_conversation()
    conversation.close()

    with pytest.raises(ValueError):
        conversation.register_activity(START + timedelta(minutes=5))

    assert conversation.last_activity_at == START
