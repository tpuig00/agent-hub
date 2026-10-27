from dataclasses import dataclass
from enum import Enum


class MessageStatus(str, Enum):
    RECEIVED = "received"
    ANSWERED = "answered"

class Channel(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"

@dataclass
class Message:
    id: str
    channel: Channel
    sender: str
    content: str
    status: MessageStatus = MessageStatus.RECEIVED
    reply: str | None = None

    def mark_as_answered(self, reply: str):
        if self.status == MessageStatus.ANSWERED:
            raise ValueError("Message is already marked as answered.")

            
        self.reply = reply
        self.status = MessageStatus.ANSWERED



