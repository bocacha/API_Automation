import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import logging
import pytest

# from Test_Framework.api.messages.test_messages import TestPlaylist
# TestPlaylist.setup_class()

LOGGER = logging.getLogger(__name__)

API_TOKEN = os.getenv('KEY')
BASE_URL = 'https://mailsac.com/api/'
FROM_ADDRESS = os.getenv('FROM_ADDRESS')
TO_ADDRESS = os.getenv('TO_ADDRESS')
SUBJECT = 'LAST FIXTURE for Mailsac SMTP Email Send'
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
message_id = None

@pytest.fixture
def create_message():
    
    BODY_TEXT = ("Mailsac SMTP Validate Email Send\r\n"
                     "This email was sent using an OFFICE365 email."
                     )
    msg = MIMEMultipart()
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg['Subject'] = SUBJECT
    msg.attach(MIMEText(BODY_TEXT, 'plain'))

    try:        
        # Connect to SMTP server and send email      
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.connect(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_ADDRESS, TO_ADDRESS, text)
        server.quit()
        LOGGER.info("Email sent successfully!")
    except Exception as e:
        LOGGER.error(f"Error sending email: {e}")
    
    # Call check_received method to get the message ID
    headers = {'Mailsac-Key': API_TOKEN}
    api_url = f'{BASE_URL}addresses/{TO_ADDRESS}/messages'
    response = requests.get(api_url, headers=headers)
    data = response.json()
    if data:
        message_id = data[0]['_id']
        LOGGER.debug(f"Message ID: {message_id}")
    else:
        LOGGER.error("No data found in response")
    #global message_id
    message_id = data[0]['_id']
    LOGGER.debug(f"Message ID: {message_id}")
    return message_id


























