from abc import ABC, abstractmethod

from app.domain.conversation import Channel, Conversation, ConversationStatus


class ConversationRepository(ABC):
    """Contrato: qué se puede hacer con las conversaciones guardadas."""

    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        ...

    @abstractmethod
    def get_open(self, channel: Channel, customer_id: str) -> Conversation | None:
        ...


class InMemoryConversationRepository(ConversationRepository):
    """Implementación simple: guarda en un diccionario. Ideal para empezar y para tests."""

    def __init__(self):
        self._conversations: dict[str, Conversation] = {}

    def save(self, conversation: Conversation) -> None:
        self._conversations[conversation.id] = conversation

    def get_open(self, channel: Channel, customer_id: str) -> Conversation | None:
        return next(
            (
                c for c in self._conversations.values()
                if c.channel == channel and c.customer_id == customer_id and c.status == ConversationStatus.OPEN
            ),
            None,
        )
