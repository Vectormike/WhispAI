from pydantic import BaseModel, Field
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv
import os

class LLMConfig(BaseModel):
    model_name: str = Field(
        default="llama3",
        description="Name of the LLM model to use",
    )
    base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL of the LLM API",
    )

@lru_cache
def get_llm_config() -> LLMConfig:
    load_dotenv()
    return LLMConfig(
        model_name=os.getenv("LLM_MODEL_NAME"),
        base_url=os.getenv("OLLAMA_BASE_URL"),
    )

