from agents import set_default_openai_key

from app.config import settings
from app.integrations.ai import OpenAIAgentResponder
from app.repositories.message_repository import InMemoryMessageRepository
from app.services.message_services import MessageService

# pydantic-settings lee el .env pero NO lo copia a os.environ, así que el SDK no encuentra la clave por su cuenta
set_default_openai_key(settings.openai_api_key)

# Único sitio donde se decide qué implementación hay detrás de cada interfaz.
# Se crea una sola vez al arrancar: si se creara en cada petición, el dict empezaría vacío siempre.
message_repository = InMemoryMessageRepository()
ai_responder = OpenAIAgentResponder(settings.openai_vector_store_id, settings.agent_model)
message_service = MessageService(message_repository, ai_responder)



def get_message_service() -> MessageService:
    return message_service
