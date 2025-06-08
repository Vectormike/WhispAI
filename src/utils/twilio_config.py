from pydantic import BaseModel, Field
from functools import lru_cache
from dotenv import load_dotenv, dotenv_values
import os


class TwilioConfig(BaseModel):
    account_sid: str = Field(..., description="Twilio Account SID")
    auth_token: str = Field(..., description="Twilio Auth Token")
    whatsapp_number: str = Field(..., description="Twilio WhatsApp Number")
    class Config:
        env_prefix = "TWILIO_"

@lru_cache
def get_twilio_config() -> TwilioConfig:
    # Find the .env file
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')

    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f".env file not found at {dotenv_path}")
    
    # Load values directly from .env file
    env_values = dotenv_values(dotenv_path)
    for k, v in env_values.items():
        if k.startswith('TWILIO_'):
            masked_value = '*' * len(v) if 'TOKEN' in k else v
            print(f"{k}: {masked_value}")
    
    account_sid = env_values.get('TWILIO_ACCOUNT_SID')
    auth_token = env_values.get('TWILIO_AUTH_TOKEN')
    whatsapp_number = env_values.get('TWILIO_WHATSAPP_NUMBER')
    
    if not all([account_sid, auth_token, whatsapp_number]):
        missing = []
        if not account_sid: missing.append("TWILIO_ACCOUNT_SID")
        if not auth_token: missing.append("TWILIO_AUTH_TOKEN")
        if not whatsapp_number: missing.append("TWILIO_WHATSAPP_NUMBER")
        raise ValueError(f"Missing required variables in .env file: {', '.join(missing)}")

    return TwilioConfig(
        account_sid=account_sid,
        auth_token=auth_token,
        whatsapp_number=whatsapp_number
    )