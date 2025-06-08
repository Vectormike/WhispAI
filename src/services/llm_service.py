from langchain_ollama import OllamaLLM
from src.utils.llm_config import get_llm_config

class LLMService:
    def __init__(self):
        self.config = get_llm_config()
        self.llm = OllamaLLM(
            model=self.config.model_name,
            base_url=self.config.base_url
        )

    async def generate_response(self, prompt: str) -> str:
        try:
            response = await self.llm.agenerate([prompt])
            return response.generations[0][0].text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I'm having trouble understanding you."