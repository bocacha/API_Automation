import logging
import os
import json
from ..utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)



abs_path = os.path.abspath(__file__ + "../../../")

class ValidateResponse: 
    # read from json file "/api/addresses/{cls.email}/messages"
    def validate_response(self, actual_response=None,  file_name=None):
        """
            :param actual_response:  REST response
        """
        LOGGER.debug("Actual response from validate: %s", actual_response)
        expected_response = self.read_input_data_json(f"{abs_path}/api/input_data/{file_name}.json")

        # compare results
        # validate status_code

        if isinstance(actual_response, list):
            actual_response = actual_response[0] 
            LOGGER.debug("ENTERING IF INSTANCE")
        self.validate_value(expected_response["subject"], actual_response["subject"], "subject")
        # validate headers
        #self.validate_value(expected_response["headers"], actual_response["headers"], "headers")
        # validate body
        #self.validate_value(expected_response["response"]["body"], actual_response["body"], "body")

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