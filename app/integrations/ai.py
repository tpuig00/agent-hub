from abc import ABC, abstractmethod

from agents import Agent, FileSearchTool, Runner

INSTRUCTIONS = """Eres el asistente de atención al cliente.
Responde de forma breve y amable, en el idioma del cliente.
Usa solo la información de los documentos. Si no la encuentras, dilo y ofrece hablar con una persona."""


class AIResponder(ABC):
    """Contrato: dado el texto del cliente, devolver una respuesta."""

    @abstractmethod
    async def reply(self, text: str) -> str:
        ...


class OpenAIAgentResponder(AIResponder):
    """Implementación con el Agents SDK de OpenAI y búsqueda en el vector store."""

    def __init__(self, vector_store_id: str, model: str):
        # El Agent es configuración: se crea una vez y se reutiliza en cada mensaje
        self.agent = Agent(
            name="Atención al cliente",
            instructions=INSTRUCTIONS,
            model=model,
            tools=[FileSearchTool(vector_store_ids=[vector_store_id], max_num_results=3)],
        )

    async def reply(self, text: str) -> str:
        result = await Runner.run(self.agent, text)
        return result.final_output
