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

import sys
sys.path.append('../helpers')
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

from Test_Framework.helpers.restClient import RestClient
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
#message_id = None


class TestAdresses:

    @classmethod
    def setup_class(cls):
        """
        Setup Class is called before the class is initiated
        """
        cls.rest_client = RestClient()
        cls.conn = http.client.HTTPSConnection("mailsac.com")
        cls.headers = { 'Mailsac-Key': key}
        cls.email = email
        cls.conn.request("GET", f"/api/addresses/", headers=cls.headers)
        res = cls.conn.getresponse()
        data = res.read()
        adresses = json.loads(data.decode("utf-8"))
        LOGGER.debug("Addresses: %s", adresses)
        if adresses:  # Check if the list is not empty
            cls.address_id = adresses[0]["_id"]
            LOGGER.debug("Address ID: %s", cls.address_id)
        else:
            LOGGER.error("No messages found.")

    def test_get_all_addresses(self):
        """
        Test Get All Messages
        """
        self.conn.request("GET", f"/api/addresses", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        addresses = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to get all owned addresses: %s", addresses)
        assert res.status == 200
        
    def test_get_address(self):
        """
        Test Get Address
        """
        self.conn.request("GET", f"/api/addresses/{self.address_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        address = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to check if owned an address: %s", address)
        assert res.status == 200

    #Create a new owned address will fail since this API request we pay for create more than 1 address
    #Thats why we will get a 400 status code
    def test_create_address(self):
        """
        Test Create Address
        """
        self.conn.request("POST", f"/api/addresses/bocacha2@mailsac.com", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        address = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to create an address: %s", address)
        assert res.status == 400

    #This code will delete the the owned property of the address
    def test_delete_address(self):
        """
        Test Delete Address
        """
        self.conn.request("DELETE", f"/api/addresses/{self.address_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()
        address = json.loads(data.decode("utf-8"))
        LOGGER.debug("Response to delete an address: %s", address)
        assert res.status == 200

