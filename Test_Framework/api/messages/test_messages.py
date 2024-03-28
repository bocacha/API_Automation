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
        cls.headers = { 'Mailsac-Key': "k_pZ2lvXIuAkvoXBi4bBm99w7djLFLkEeunR6fImwwd4" }
        cls.email = email

    def test_get_all_messages(self):
        """
        Test Get All Messages
        """
        self.conn.request("GET", f"/api/addresses/{self.email}/messages", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        messages = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to get all messages: %s", messages)
        assert res.status == 200, "Response code is not 200"
        assert isinstance(messages, list), "Response content is not a list of messages"