from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_sms(to_number, message):
    client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to="+91"+to_number 
    )