import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

load_dotenv()
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
EMAIL = os.environ.get('EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


class NotificationManager:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

    def send_sms(self, message):
        message = message
        self.client.messages \
            .create(
            body=message,
            from_=TWILIO_NUMBER,
            to='+916281646095',
        )
        return "Done"

    def send_emails(self, message, receiver_email):
        subject = 'Flight Best Deal'
        with self.server as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=EMAIL_PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=receiver_email,
                                msg=f"Subject:{subject}\n\n{message}")
        return "sent"
