from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from src.utils.twilio_config import get_twilio_config
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        try:
            self.config = get_twilio_config()
            print(self.config.account_sid, "account sid")
            print(self.config.auth_token, "auth token")
            
            self.client = Client(
                self.config.account_sid,
                self.config.auth_token
            )
            
            # Test the credentials
            self.client.api.accounts(self.config.account_sid).fetch()
            logger.info("Successfully initialized WhatsApp service")
            
        except TwilioRestException as e:
            logger.error(f"Twilio authentication error: {str(e)}")
            raise ValueError(f"Failed to initialize WhatsApp service: {str(e)}")
        except Exception as e:
            logger.error(f"Error initializing WhatsApp service: {str(e)}")
            raise

    async def send_message(self, to: str, body: str) -> None:
        try:
            # Format the WhatsApp number if needed
            to_number = f"whatsapp:{to}" if not to.startswith("whatsapp:") else to
            from_number = f"whatsapp:{self.config.whatsapp_number}" if not self.config.whatsapp_number.startswith("whatsapp:") else self.config.whatsapp_number
            
            logger.debug(f"Sending WhatsApp message from {from_number} to {to_number}")
            message = self.client.messages.create(
                from_=from_number,
                body=body,
                to=to_number
            )
            logger.info(f"Message sent successfully with SID: {message.sid}")
            
        except TwilioRestException as e:
            logger.error(f"Twilio error sending message: {str(e)}")
            raise ValueError(f"Error sending WhatsApp message: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error sending message: {str(e)}")
            raise ValueError(f"Error sending message: {str(e)}")

        # message = self.client.messages.create(
        #     from_='whatsapp:+14155238886',
        #     content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
        #     content_variables='{"1":"12/1","2":"3pm"}',
        #     to='whatsapp:+2348086249721'
        # )