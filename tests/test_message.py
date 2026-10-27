from app.domain.message import Direction, Message, MessageStatus


def test_inbound_message_is_received_and_keeps_external_id():
    message = Message.inbound("conv-1", "Hola", "wamid.1")

    assert message.direction == Direction.INBOUND
    assert message.status == MessageStatus.RECEIVED
    assert message.external_id == "wamid.1"


def test_outbound_message_is_pending_and_has_no_external_id_yet():
    message = Message.outbound("conv-1", "¡Hola! ¿En qué te ayudo?")

    assert message.direction == Direction.OUTBOUND
    assert message.status == MessageStatus.PENDING
    assert message.external_id is None


def test_each_message_gets_its_own_id():
    assert Message.outbound("conv-1", "a").id != Message.outbound("conv-1", "a").id
