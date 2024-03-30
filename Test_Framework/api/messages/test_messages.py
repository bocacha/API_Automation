import logging
import os
import sys
import requests
import http.client
import json

from dotenv import load_dotenv
from ...utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

# Load client_id and client_secret from the environment variables:

load_dotenv()

email = os.getenv("EMAIL")
key = os.getenv("KEY")


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
        LOGGER.debug("Response to get all messages: %s", messages)
        #show the logger message in JSON format:
        LOGGER.info("Response to get all messages: %s", json.dumps(messages, indent=2))
        assert res.status == 200, "Response code is not 200"
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
        assert isinstance(count, int), "Response content is not an integer"
        
    def test_move_message(self):
        """
        Test Move Message
        """
        self.conn.request("PUT", f"/api/addresses/{self.email}/messages/{self.message_id}/folder/trash", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        message = json.loads(data.decode("utf-8"))
        folder_moved = message["folder"]
        message_sender = message["from"][0]["address"]
        message_subject = message["subject"]
        LOGGER.debug("Response to move message: %s", message)
        #Describe in the Logger message id, message sender, message subject and to wich folder the message was moved:
        LOGGER.info("The message ID: %s,  received from: %s, with the Subject: %s, was moved to the folder: %s", self.message_id, message_sender, message_subject, folder_moved)
        assert res.status == 200, "Response code is not 200"
        assert isinstance(message, dict), "Response content is not a message"