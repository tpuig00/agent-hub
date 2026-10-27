from abc import ABC, abstractmethod

from agents import Agent, FileSearchTool, OpenAIConversationsSession, Runner
from openai import AsyncOpenAI

INSTRUCTIONS = """Eres el asistente de atención al cliente.
Responde de forma breve y amable, en el idioma del cliente.
Usa solo la información de los documentos. Si no la encuentras, dilo y ofrece hablar con una persona."""


class AIResponder(ABC):
    """Contrato: abrir una conversación con la IA y responder dentro de ella (con memoria de lo anterior)."""

    @abstractmethod
    async def start_conversation(self) -> str:
        ...

    @abstractmethod
    async def reply(self, ai_conversation_id: str, text: str) -> str:
        ...


class OpenAIAgentResponder(AIResponder):
    """Implementación con el Agents SDK de OpenAI, búsqueda en el vector store y la Conversations API como memoria."""

    def __init__(self, client: AsyncOpenAI, vector_store_id: str, model: str):
        self.client = client
        # El Agent es configuración: se crea una vez y se reutiliza en cada mensaje
        self.agent = Agent(
            name="Atención al cliente",
            instructions=INSTRUCTIONS,
            model=model,
            tools=[FileSearchTool(vector_store_ids=[vector_store_id], max_num_results=3)],
        )

    async def start_conversation(self) -> str:
        # La creamos nosotros (y no la sesión) porque necesitamos su id para guardarlo en nuestra Conversation
        conversation = await self.client.conversations.create()
        return conversation.id

    async def reply(self, ai_conversation_id: str, text: str) -> str:
        # La sesión lee el historial de esa conversación en OpenAI y le añade el turno nuevo
        session = OpenAIConversationsSession(conversation_id=ai_conversation_id, openai_client=self.client)
        result = await Runner.run(self.agent, text, session=session)
        return result.final_output
