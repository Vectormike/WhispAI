from langchain_ollama import OllamaLLM
from src.core.llm_config import get_llm_config
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel, PeftConfig
import torch
import logging
import os
import tempfile

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        try:
            self.config = get_llm_config()
            
            # Create a temporary directory for model offloading
            self.offload_dir = os.path.join(tempfile.gettempdir(), "model_offload")
            os.makedirs(self.offload_dir, exist_ok=True)
            logger.info(f"Created offload directory at: {self.offload_dir}")
            
            # Configure device mapping
            if torch.backends.mps.is_available():
                device_map = {"": "cpu"}  # Force CPU for MPS devices
            else:
                device_map = "auto"
            
            logger.info("Loading base model...")
            base_model = AutoModelForCausalLM.from_pretrained(
                "meta-llama/Llama-3.1-8B",
                torch_dtype=torch.float16,
                device_map=device_map,
                offload_folder=self.offload_dir,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            logger.info("Base model loaded successfully")

            logger.info("Loading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(
                "Jammies-io/livestockmodel-llama",
                subfolder="output",
                trust_remote_code=True
            )
            logger.info("Tokenizer loaded successfully")

            logger.info("Loading PEFT model...")
            try:
                # First check PEFT config
                peft_config = PeftConfig.from_pretrained(
                    "Jammies-io/livestockmodel-llama",
                    subfolder="output"
                )
                logger.info(f"PEFT config loaded: {peft_config}")

                # Try loading with merge_and_unload
                model = PeftModel.from_pretrained(
                    base_model,
                    "Jammies-io/livestockmodel-llama",
                    subfolder="output",
                    offload_folder=self.offload_dir,
                    trust_remote_code=True
                )
                model = model.merge_and_unload()
                logger.info("PEFT model loaded and merged successfully")
            except Exception as peft_error:
                logger.error(f"Error loading PEFT model: {str(peft_error)}")
                # Fallback to using base model if PEFT loading fails
                logger.info("Falling back to base model...")
                model = base_model

            logger.info("Initializing pipeline...")
            self.pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device_map=device_map,
                model_kwargs={"torch_dtype": torch.float16}
            )
            logger.info("Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing LLM service: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {str(e)}")
            raise ValueError(f"Failed to initialize LLM service: {str(e)}")

    async def generate_response(self, prompt: str) -> str:
        try:
            logger.info(f"Generating response for prompt: {prompt[:50]}...")
            
            # Generate response
            response = self.pipeline(
                prompt,
                max_new_tokens=256,  # Control the length of generated text
                num_return_sequences=1,
                truncation=True,
                temperature=0.7,  # Add some randomness to the output
                do_sample=True,  # Enable sampling for more natural responses
                pad_token_id=self.pipeline.tokenizer.eos_token_id
            )
            
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