from typing import Optional
from datetime import datetime
from fastapi import Depends
from src.services.llm_service import LLMService
from src.services.whatsapp_service import WhatsAppService

class MessageService:
    def __init__(
        self,
        llm_service: LLMService = Depends(LLMService),
        whatsapp_service: WhatsAppService = Depends(WhatsAppService)
    ):
        self.llm_service = llm_service
        self.whatsapp_service = whatsapp_service

    async def process_message(self, message: str, sender: str) -> str:
        try:
            # Generate response using LLM
            response = await self.llm_service.generate_response(message)
            
            # Send response via WhatsApp
            await self.whatsapp_service.send_message(to=sender, body=response)
            
            return response
        except Exception as e:
            print(f"Error in process_message: {e}")
            raise e
