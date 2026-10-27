import logging
from datetime import UTC, datetime, timedelta

from app.domain.conversation import Channel, Conversation
from app.domain.message import Message
from app.integrations.ai import AIResponder
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

logger = logging.getLogger(__name__)


class MessageService:
    """Casos de uso de los mensajes. Orquesta el dominio, los repositorios y la IA."""

    def __init__(
        self,
        messages: MessageRepository,
        conversations: ConversationRepository,
        ai_responder: AIResponder,
        conversation_timeout: timedelta,
    ):
        self.messages = messages
        self.conversations = conversations
        self.ai_responder = ai_responder
        self.conversation_timeout = conversation_timeout

    async def receive(self, external_id: str, channel: Channel, customer_id: str, content: str) -> Message | None:
        """Guarda el mensaje del cliente y devuelve nuestra respuesta, o None si ya lo habíamos procesado."""
        # WhatsApp puede reenviar el mismo webhook: si ya lo tenemos, no lo procesamos otra vez
        if self.messages.get_by_external_id(external_id):
            logger.info("Mensaje %s duplicado: se ignora", external_id)
            return None

        now = datetime.now(UTC)
        conversation = await self._get_or_start_conversation(channel, customer_id, now)

        self.messages.save(Message.inbound(conversation.id, content, external_id))

        reply = await self.ai_responder.reply(conversation.ai_conversation_id, content)
        outbound = Message.outbound(conversation.id, reply)
        self.messages.save(outbound)

        conversation.register_activity(now)
        self.conversations.save(conversation)
        logger.info("Mensaje %s respondido en la conversación %s", external_id, conversation.id)
        return outbound

    async def _get_or_start_conversation(self, channel: Channel, customer_id: str, now: datetime) -> Conversation:
        conversation = self.conversations.get_open(channel, customer_id)

        # La caducidad se comprueba al llegar el siguiente mensaje, sin cron (como la session lifetime de Laravel)
        if conversation and conversation.is_expired(now, self.conversation_timeout):
            conversation.close()
            self.conversations.save(conversation)
            conversation = None

        if conversation is None:
            ai_conversation_id = await self.ai_responder.start_conversation()
            conversation = Conversation.start(channel, customer_id, ai_conversation_id, now)
            self.conversations.save(conversation)

        return conversation

    def get(self, message_id: str) -> Message | None:
        return self.messages.get_by_id(message_id)
