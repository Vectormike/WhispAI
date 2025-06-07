from pydantic import BaseModel, Field
from functools import lru_cache
from dotenv import load_dotenv
import os


class TwilioConfig(BaseModel):
    account_sid: str = Field(..., env="TWILIO_ACCOUNT_SID")
    auth_token: str = Field(..., env="TWILIO_AUTH_TOKEN")
    whatsapp_number: str = Field(..., env="TWILIO_WHATSAPP_NUMBER")

@lru_cache
def get_twilio_config() -> TwilioConfig:

    load_dotenv()

    return TwilioConfig(
        account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
        auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
        whatsapp_number=os.getenv("TWILIO_WHATSAPP_NUMBER"),
    )