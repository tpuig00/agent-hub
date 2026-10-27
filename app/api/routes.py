from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from app.dependencies import get_message_service
from app.domain.conversation import Channel
from app.domain.message import Direction, Message, MessageStatus
from app.services.message_services import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


# Esquemas HTTP: definen qué entra y qué sale por la API. No son el dominio.
class ReceiveMessageRequest(BaseModel):
    external_id: str
    channel: Channel = Channel.WHATSAPP
    customer_id: str
    content: str


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    direction: Direction
    content: str
    status: MessageStatus
    external_id: str | None = None

    @classmethod
    def from_domain(cls, message: Message) -> "MessageResponse":
        return cls(
            id=message.id,
            conversation_id=message.conversation_id,
            direction=message.direction,
            content=message.content,
            status=message.status,
            external_id=message.external_id,
        )


@router.post("", response_model=MessageResponse, status_code=201)
async def receive_message(
    body: ReceiveMessageRequest,
    service: MessageService = Depends(get_message_service),
):
    reply = await service.receive(body.external_id, body.channel, body.customer_id, body.content)
    if reply is None:
        # Duplicado: 200 para que WhatsApp no lo reintente, pero sin crear nada nuevo
        return Response(status_code=200)
    return MessageResponse.from_domain(reply)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: str,
    service: MessageService = Depends(get_message_service),
):
    message = service.get(message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return MessageResponse.from_domain(message)
