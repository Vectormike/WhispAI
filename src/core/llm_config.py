from pydantic import BaseModel, Field
from functools import lru_cache
from dotenv import load_dotenv
import os

class LLMConfig(BaseModel):
    model_name: str = Field(
        default="meta-llama/Llama-2-7b-chat-hf",
        description="Name of the Hugging Face model to use",
    )
    temperature: float = Field(
        default=0.7,
        description="Sampling temperature",
    )
    top_p: float = Field(
        default=0.95,
        description="Top p sampling parameter",
    )
    max_length: int = Field(
        default=512,
        description="Maximum sequence length",
    )
    hf_token: str = Field(
        default="",
        description="Hugging Face API token for accessing gated models",
    )

@lru_cache
def get_llm_config() -> LLMConfig:
    load_dotenv()
    return LLMConfig(
        model_name=os.getenv("HF_MODEL_NAME", "meta-llama/Llama-2-7b-chat-hf"),
        temperature=float(os.getenv("HF_TEMPERATURE", "0.7")),
        top_p=float(os.getenv("HF_TOP_P", "0.95")),
        max_length=int(os.getenv("HF_MAX_LENGTH", "512")),
        hf_token=os.getenv("HF_TOKEN", "")
    )