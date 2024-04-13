import logging
import os
import json

from dotenv import load_dotenv
from utils.logger import get_logger

abs_path = os.path.abspath(__file__ + "../../../")

LOGGER = get_logger(__name__, logging.DEBUG)

load_dotenv()

email = os.getenv("EMAIL")

class ValidateResponse: 
    # read from json file "/api/addresses/{cls.email}/messages"
    def validate_response(self, actual_response=None, endpoint=None, file_name=None):
        """
            :param actual_response:  REST response
            :param endpoint:         endpoint used i.e projects
        """
        expected_response = self.read_input_data_json(f"{abs_path}/api/addresses/{email}{endpoint}/{file_name}.json")

        # compare results
        # validate status_code
        self.validate_value(expected_response["status_code"], actual_response["status_code"], "status_code")
        # validate headers
        self.validate_value(expected_response["headers"], actual_response["headers"], "headers")
        # validate body
        self.validate_value(expected_response["response"]["body"], actual_response["body"], "body")

    def validate_value(self, expected_value, actual_value, key_compare):
        error_message = f"Expected '{expected_value}' but received '{actual_value}'"
        LOGGER.debug("Expected '%s': '%s'", key_compare, expected_value)
        LOGGER.debug("Actual '%s': %s", key_compare, actual_value)
        if key_compare == "body":
            if isinstance(actual_value, list):
                assert self.compare_json_keys(expected_value[0], actual_value[0]), error_message
            else:
                assert self.compare_json_keys(expected_value, actual_value), error_message
        elif key_compare == "headers":
            assert expected_value.items() <= actual_value.items()
        else:
            assert expected_value == actual_value, error_message

    @staticmethod
    def read_input_data_json(file_name):
        """
        :param file_name: 
        :return: 
        """
        LOGGER.debug("Reading input data from file: %s", file_name)
        with open(file_name) as json_file:
            data = json.load(json_file)
            LOGGER.debug("Data from file: %s", data)
        json_file.close()

        return data
    
    @staticmethod
    def compare_json_keys(json1, json2):
        """

        :param json1:
        :param json2:
        :return:  boolean   True if json1 == json2
        """
        for key in json1.keys():
            if key in json2.keys():
                LOGGER.debug("Key '%s' found in json2", key)
            else:
                LOGGER.debug("Key '%s' not found in json2", key)
                return  False
        return True

if __name__ == "__main__":
    val=ValidateResponse()
    val.validate_response()