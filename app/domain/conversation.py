from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4


class Channel(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"


class ConversationStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass
class Conversation:
    id: str
    channel: Channel
    customer_id: str          # BSUID en WhatsApp, dirección en email
    ai_conversation_id: str   # "conv_..." de OpenAI: para el dominio es solo un texto
    last_activity_at: datetime
    customer_name: str | None = None
    status: ConversationStatus = ConversationStatus.OPEN

    @classmethod
    def start(cls, channel: Channel, customer_id: str, ai_conversation_id: str, now: datetime) -> "Conversation":
        return cls(str(uuid4()), channel, customer_id, ai_conversation_id, last_activity_at=now)

    def is_expired(self, now: datetime, timeout: timedelta) -> bool:
        return now - self.last_activity_at > timeout

    def register_activity(self, now: datetime):
        if self.status == ConversationStatus.CLOSED:
            raise ValueError("Conversation is closed.")

        self.last_activity_at = now

    def close(self):
        self.status = ConversationStatus.CLOSED
