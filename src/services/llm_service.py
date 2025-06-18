from langchain_ollama import OllamaLLM
from src.core.llm_config import get_llm_config
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel
import torch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        try:
            self.config = get_llm_config()

            # Load base model (set to meta-llama/Llama-3.1-8B)
            base_model = AutoModelForCausalLM.from_pretrained(
                "meta-llama/Llama-3.1-8B",
                torch_dtype=torch.float16,
                device_map="auto"
            )

            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                "Jammies-io/livestockmodel-llama",
                subfolder="output"
            )

            # Load your LoRA adapter
            model = PeftModel.from_pretrained(
                base_model,
                "Jammies-io/livestockmodel-llama",
                subfolder="output"
            )

            self.pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
            )
            logger.info("Model and pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing LLM service: {str(e)}")
            raise ValueError(f"Failed to initialize LLM service: {str(e)}")

    async def generate_response(self, prompt: str) -> str:
        try:
            logger.info(f"Generating response for prompt: {prompt[:50]}...")
            response = self.pipeline(
                prompt,
                max_new_tokens=256,
                num_return_sequences=1,
                truncation=True,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.pipeline.tokenizer.eos_token_id
            )
            if response and isinstance(response, list) and len(response) > 0:
                generated_text = response[0]['generated_text']
                logger.info(f"Generated response: {generated_text[:50]}...")
                return generated_text
            else:
                raise ValueError("Invalid response format from pipeline")
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Sorry, I'm having trouble understanding you."