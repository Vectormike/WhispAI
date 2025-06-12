from langchain_ollama import OllamaLLM
from src.core.llm_config import get_llm_config
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, LlamaTokenizer, LlamaForCausalLM
import torch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        try:
            self.config = get_llm_config()
            model_id = "Jammies-io/livestockmodel-llama"

            logger.info(f"Initializing model {model_id}")
            
            self.tokenizer = LlamaTokenizer.from_pretrained(model_id)
            self.model = LlamaForCausalLM.from_pretrained(model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto"
            )

            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
            )
            logger.info("Model and pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing LLM service: {str(e)}")
            raise ValueError(f"Failed to initialize LLM service: {str(e)}")

    async def generate_response(self, prompt: str) -> str:
        try:
            if not isinstance(prompt, str):
                raise ValueError("Prompt must be a string")
                
            logger.info(f"Generating response for prompt: {prompt[:50]}...")
            
            # Generate response
            response = self.pipeline(prompt)
            
            # Extract the generated text from the response
            if response and isinstance(response, list) and len(response) > 0:
                # Access the first element directly since it's a list of dictionaries
                generated_text = response[0]['generated_text']
                logger.info(f"Generated response: {generated_text[:50]}...")
                return generated_text
            else:
                raise ValueError("Invalid response format from pipeline")
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Sorry, I'm having trouble understanding you."