import json
import requests
import logging

#import get_logger from logger.py located in utils folder under Test_Framework

from ..utils.logger import get_logger


HEADER = { 'Mailsac-Key': 'k_pZ2lvXIuAkvoXBi4bBm99w7djLFLkEeunR6fImwwd4'}
LOGGER = logging.getLogger(__name__)

class RestClient:
    """
    RestClient class to handle REST API requests
    """
    def __init__(self, headers=HEADER):
        self.session = requests.Session()
        self.session.headers.update(headers)

    def request(self, method_name, url, body=None, headers=None):
        """
        :param method_name: 
        :param url: 
        :param body:
        :param headers: 
        :return: 
        """
        """
        response['status_code'] 
        response['headers']
        response['body']
        """
        if headers:
             self.session.headers.update(headers)
        response = self.select_method(method_name, self.session)(url=url, data=body)
        LOGGER.debug("Response to (JSON): %s", response.json())
        LOGGER.debug("Status code: %s", response.status_code)
        return response
    
    @staticmethod
    def select_method(method_name, session):
        """
        Select REST method with session object
        :param method_name: 
        :param session:
        :return: 
        """
        methods = {
            "get": session.get,
            "post": session.post,
            "put": session.put,
            "delete": session.delete
        }

        return methods.get(method_name)
    

