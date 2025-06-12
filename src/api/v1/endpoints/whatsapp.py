from fastapi import APIRouter, Request, HTTPException, Depends
from src.services.message_service import MessageService
import logging
from typing import Dict, Any

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook", response_model=Dict[str, Any])
async def whatsapp_webhook(
    request: Request,
    message_service: MessageService = Depends(MessageService),
) -> Dict[str, Any]:
    try:
        # Try to get the data in various formats
        content_type = request.headers.get("content-type", "").lower()
        
        if "application/json" in content_type:
            data = await request.json()
        elif "application/x-www-form-urlencoded" in content_type:
            form_data = await request.form()
            data = dict(form_data)
        else:
            # Log the unexpected content type
            logger.error(f"Unexpected content type: {content_type}")
            raw_body = await request.body()
            logger.error(f"Raw request body: {raw_body}")
            raise HTTPException(status_code=400, detail="Unsupported content type")

        logger.info(f"Received webhook data: {data}")
        
        # Extract message and sender from the data
        message = data.get("Body")
        sender = data.get("From")

        logger.info(f"Extracted message: {message}")
        logger.info(f"Extracted sender: {sender}")
        
        if not message or not sender:
            logger.error(f"Missing required fields. Data received: {data}")
            raise HTTPException(status_code=400, detail="Missing message or sender")
            
        response = await message_service.process_message(message, sender)
        return {"status": "success", "response": response}
    
    except HTTPException as e:
        # Re-raise HTTP exceptions as is
        raise e
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing message")