from typing import Optional
from datetime import datetime
from src.services.llm_service import LLMService
from src.services.whatsapp_service import WhatsAppService

class MessageService:
    def __init__(self, llm_service: LLMService, whatsapp_service: WhatsAppService):
        self.llm_service = llm_service
        self.whatsapp_service = whatsapp_service

    async def process_message(self, message: str, sender: str, ):
        response = self.llm_service.generate_response(message)
        print(response)
