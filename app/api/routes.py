from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.dependencies import get_message_service
from app.domain.message import Channel, Message, MessageStatus
from app.services.message_services import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


# Esquemas HTTP: definen qué entra y qué sale por la API. No son el dominio.
class ReceiveMessageRequest(BaseModel):
    id: str
    channel: Channel = Channel.WHATSAPP
    sender: str
    content: str


class MessageResponse(BaseModel):
    id: str
    channel: Channel
    sender: str
    content: str
    status: MessageStatus
    reply: str | None = None

    @classmethod
    def from_domain(cls, message: Message) -> "MessageResponse":
        return cls(
            id=message.id,
            channel=message.channel,
            sender=message.sender,
            content=message.content,
            status=message.status,
            reply=message.reply
        )


@router.post("", response_model=MessageResponse, status_code=201)
async def receive_message(
    body: ReceiveMessageRequest,
    service: MessageService = Depends(get_message_service),
):
    message = await service.receive(body.id, body.channel, body.sender, body.content)
    return MessageResponse.from_domain(message)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: str,
    service: MessageService = Depends(get_message_service),
):
    message = service.get(message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return MessageResponse.from_domain(message)
