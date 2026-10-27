from app.domain.message import Channel, Message
from app.repositories.message_repository import MessageRepository


class MessageService:
    """Casos de uso de los mensajes. Orquesta el dominio y el repositorio."""

    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def receive(self, message_id: str, channel: Channel, sender: str, content: str) -> Message:
        # WhatsApp puede reenviar el mismo webhook: si ya lo tenemos, no lo duplicamos
        existing = self.repository.get_by_id(message_id)
        if existing:
            return existing

        message = Message(id=message_id, channel=channel, sender=sender, content=content)
        self.repository.save(message)
        return message

    def get(self, message_id: str) -> Message | None:
        return self.repository.get_by_id(message_id)
