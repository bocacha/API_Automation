import logging
import os
import sys
import requests
import http.client
import json

import time
import email.utils
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from ...utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

# Load client_id and client_secret from the environment variables:

load_dotenv()

email = os.getenv("EMAIL")
key = os.getenv("KEY")

API_TOKEN = os.getenv('KEY')
BASE_URL = 'https://mailsac.com/api/'
FROM_ADDRESS = os.getenv('FROM_ADDRESS')
TO_ADDRESS = os.getenv('TO_ADDRESS')
SUBJECT = 'FROM test_create_message Validate Email Send'
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

my_id = None

class TestPlaylist:

    @classmethod
    def setup_class(cls):
        """
        Setup Class is called before the class is initiated
        """
        cls.conn = http.client.HTTPSConnection("mailsac.com")
        cls.headers = { 'Mailsac-Key': key}
        cls.email = email
        cls.conn.request("GET", f"/api/addresses/{cls.email}/messages", headers=cls.headers)
        res = cls.conn.getresponse()
        data = res.read()
        cls.message_id = json.loads(data.decode("utf-8"))[0]["_id"]
        LOGGER.debug("Message ID: %s", cls.message_id)

    def test_get_all_messages(self):
        """
        Test Get All Messages
        """
        self.conn.request("GET", f"/api/addresses/{self.email}/messages", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        messages = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to get all messages(Text): %s", messages)
        #show the logger message in JSON format:
        LOGGER.info("Response to get all messages(JSON): %s", json.dumps(messages, indent=2))
        assert res.status == 200, "Response code is not 200"
        LOGGER.debug("Status code: %s", res.status)
        assert isinstance(messages, list), "Response content is not a list of messages"

    def test_get_message(self):
        """
        Test Get Message
        """
        self.conn.request("GET", f"/api/addresses/{self.email}/messages/{self.message_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        message = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to get message: %s", message)
        assert res.status == 200, "Response code is not 200"
        LOGGER.debug("Status code: %s", res.status)
        assert isinstance(message, dict), "Response content is not a message"

        
    def test_count_messages(self):
        """
        Test Count Messages
        """
        self.conn.request("GET", f"/api/addresses/{self.email}/message-count", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        count = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to count messages: %s", count)
        assert res.status == 200, "Response code is not 200"
        LOGGER.debug("Status code: %s", res.status)
        
    def test_move_message(self):
        """
        Test Move ( Update )Message
        """
        self.conn.request("PUT", f"/api/addresses/{self.email}/messages/{self.message_id}/folder/trash", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        message = json.loads(data.decode("utf-8"))
        folder_moved = message["folder"]
        message_sender = message["from"][0]["address"]
        message_subject = message["subject"]
        LOGGER.debug("Response to move (update) message: %s", message)
        LOGGER.info("The message ID: %s,  received from: %s, with the Subject: %s, was moved to the folder: %s", self.message_id, message_sender, message_subject, folder_moved)
        assert res.status == 200, "Response code is not 200"
        LOGGER.debug("Status code: %s", res.status)
        assert isinstance(message, dict), "Response content is not a message"


    def test_create_message(self):
        """
        Test Create Message
        """
        BODY_TEXT = ("Mailsac SMTP Validate Email Send\r\n"
                     "This email was sent using an OFFICE365 email."
                     )
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        msg['From'] = FROM_ADDRESS
        msg['To'] = TO_ADDRESS
        msg['Subject'] = SUBJECT

        # Attach body to the email
        msg.attach(MIMEText(BODY_TEXT, 'plain'))

        # Connect to SMTP server and send email
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(FROM_ADDRESS, TO_ADDRESS, text)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Error: unable to send email -", e)
            raise e
        time.sleep(10)

    @staticmethod
    def check_received(receive_address, send_address, base_url, headers):
        api_url = '{0}/addresses/{1}/messages'.format(base_url, receive_address)
        response = requests.get(api_url, headers=headers)
        LOGGER.debug("***************************************Response to check received: %s", response.json())
        data = response.json()
        my_id = data[0]['_id']
        LOGGER.debug("***************************************MSG ID IS: %s", my_id)
        for message in response.json():
            if message['from'][0]['address'] == send_address:
                return message['received']
        return '{0} has not received an email from {1}'.format(receive_address, send_address)

    def test_check_received(self):
        result = self.check_received('bocacha@mailsac.com', send_address=FROM_ADDRESS,
                                     base_url=BASE_URL, headers={'Mailsac-Key': API_TOKEN})
        #Logger must detail the email sender, the message id and the time the email was received:

        LOGGER.info("The email from %s was received at %s", FROM_ADDRESS, result)

        LOGGER.debug("Mail received: %s", result)   

    def test_delete_message(self,create_message):
        """
        Test Delete Message
        """
        LOGGER.info("Test Delete Message")
        LOGGER.debug("ID message created from fixture: %s", create_message)
        time.sleep(10)
        self.conn.request("DELETE", f"/api/addresses/{self.email}/messages/{create_message}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        message = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to delete message:%s", message)
        # assert res.status == 200, "Response code is not 200"
        # LOGGER.debug("Status code: %s", res.status)

    
                                        


                          
