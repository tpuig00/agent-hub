from app.repositories.message_repository import InMemoryMessageRepository
from app.services.message_services import MessageService

# Único sitio donde se decide qué implementación hay detrás de cada interfaz.
# Se crea una sola vez al arrancar: si se creara en cada petición, el dict empezaría vacío siempre.
message_repository = InMemoryMessageRepository()
message_service = MessageService(message_repository)


def get_message_service() -> MessageService:
    return message_service
