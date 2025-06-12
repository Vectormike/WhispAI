from twilio.rest import Client
from src.core.twilio_config import get_twilio_config


class WhatsAppService:
    def __init__(self):
        self.config = get_twilio_config()
        self.client = Client(
            self.config.account_sid,
            self.config.auth_token
        )
        

    async def send_message(self, to: str, body: str) -> None:
        print(self.config.account_sid, "account sid")
        print(self.config.auth_token, "auth token")
        print(body, "body")
        try:
            message = self.client.messages.create(
                from_='whatsapp:+14155238886',
                body=body,
                to='whatsapp:+2348086249721'
            )
            print(message.sid, "message sent")
        except Exception as e:
            print(f"Error sending message: {e}")

        # message = self.client.messages.create(
        #     from_='whatsapp:+14155238886',
        #     content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
        #     content_variables='{"1":"12/1","2":"3pm"}',
        #     to='whatsapp:+2348086249721'
        # )