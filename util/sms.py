import os
from dotenv import load_dotenv
import smtplib


load_dotenv()

EMAIL = os.getenv('EMAIL')  # email to send via
PASSWORD = os.getenv('PASSWORD')  # special auth password for email above
PHONE_NUMBER = os.getenv('PHONE_NUMBER')  #  phone number to send texts to

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}


def send_text(message, phone_number=PHONE_NUMBER, carrier='att'):
    recipient = f'{phone_number}{CARRIERS[carrier]}'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    server.sendmail(EMAIL, recipient, message)


if __name__ == '__main__':
    send_text("this is a test text.")
