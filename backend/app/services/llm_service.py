from langchain_ollama import ChatOllama

from backend.app.config import settings


class LLMService:

    def __init__(self):

        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.2
        )

    def generate_response(self, prompt: str) -> str:
        """
        Generate an AI response using the configured Ollama model.
        """

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.llm.invoke(prompt)

        return response.content


llm_service = LLMService()