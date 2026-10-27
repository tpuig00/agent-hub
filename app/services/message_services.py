import logging

from app.domain.message import Channel, Message
from app.integrations.ai import AIResponder
from app.repositories.message_repository import MessageRepository

logger = logging.getLogger(__name__)


class MessageService:
    """Casos de uso de los mensajes. Orquesta el dominio y el repositorio."""

    def __init__(self, repository: MessageRepository, ai_responder: "AIResponder"):
        self.repository = repository
        self.ai_responder = ai_responder

    async def receive(self, message_id: str, channel: Channel, sender: str, content: str) -> Message:
        # WhatsApp puede reenviar el mismo webhook: si ya lo tenemos, no lo duplicamos
        existing = self.repository.get_by_id(message_id)
        if existing:
            logger.info("Mensaje %s duplicado: se devuelve el existente", message_id)
            return existing

        message = Message(id=message_id, channel=channel, sender=sender, content=content)
        self.repository.save(message)

        reply = await self.ai_responder.reply(content)
        message.mark_as_answered(reply)
        self.repository.save(message)
        logger.info("Mensaje %s respondido", message_id)
        return message

    def get(self, message_id: str) -> Message | None:
        return self.repository.get_by_id(message_id)
