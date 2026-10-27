from dataclasses import dataclass
from enum import Enum
from uuid import uuid4


class Direction(str, Enum):
    INBOUND = "inbound"    # lo escribe el cliente
    OUTBOUND = "outbound"  # lo respondemos nosotros


class MessageStatus(str, Enum):
    RECEIVED = "received"
    PENDING = "pending"    # respuesta generada, todavía sin enviar al canal


@dataclass
class Message:
    id: str
    conversation_id: str
    direction: Direction
    content: str
    status: MessageStatus
    external_id: str | None = None  # wamid o id de Gmail; una respuesta no lo tiene hasta que se envía

    # Constructores con nombre: así no se puede crear una respuesta con estado "received" ni al revés
    @classmethod
    def inbound(cls, conversation_id: str, content: str, external_id: str) -> "Message":
        return cls(str(uuid4()), conversation_id, Direction.INBOUND, content, MessageStatus.RECEIVED, external_id)

    @classmethod
    def outbound(cls, conversation_id: str, content: str) -> "Message":
        return cls(str(uuid4()), conversation_id, Direction.OUTBOUND, content, MessageStatus.PENDING)
