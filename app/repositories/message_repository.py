from abc import ABC, abstractmethod

from app.domain.message import Message

class MessageRepository(ABC):
    """Contrato: qué se puede hacer con los mensajes guardados."""

    @abstractmethod
    def save(self, message: Message) -> None:
        ...

    @abstractmethod
    def get_by_id(self, message_id: str) -> Message | None:
        ...

    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Message | None:
        ...


class InMemoryMessageRepository(MessageRepository):
    """Implementación simple: guarda en un diccionario. Ideal para empezar y para tests."""

    def __init__(self):
        self._messages: dict[str, Message] = {}

    def save(self, message: Message) -> None:
        self._messages[message.id] = message

    def get_by_id(self, message_id: str) -> Message | None:
        return self._messages.get(message_id)

    def get_by_external_id(self, external_id: str) -> Message | None:
        return next((m for m in self._messages.values() if m.external_id == external_id), None)
