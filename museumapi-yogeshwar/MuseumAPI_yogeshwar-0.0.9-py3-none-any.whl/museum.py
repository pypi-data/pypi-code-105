import requests
import logging


logging.basicConfig(filename='logging_file.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class MuseumAPI:
    """
    MuseumAPI class to get response from API
    """
    def __init__(self):
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.base_url = "https://collectionapi.metmuseum.org/public/collection/v1/"

    def get_response(self, endpoint):
        """
        :param endpoint: API endpoint
        :return : response object
        """
        try:

            url = self.base_url+endpoint
            response = requests.get(url, headers=self.headers)
        except (requests.ConnectionError, requests.Timeout, requests.ConnectTimeout) as ce:
            logging.error("Error occurred while getting response: " + str(ce))
        except requests.HTTPError as he:
            logging.error("Error occurred while getting response: " + str(he))

        return response

    def get_object_ids(self):
        """
        It will get all object ids from museum API
        :return : It will return object ids in a dictionary
        :keys: * total: int
            count of object ids
                * object ids: list
            list of object ids
        """
        endpoint = "objects"
        response = self.get_response(endpoint).json()
        if response.ok:
            return response.json()
        else:
            return None

    def get_object_for_ids(self, object_id):
        """
        It will get an object with specified object ids
        :param object_id: object_id of the object
        :return : Dictionary containing objects
        """

        endpoint = "objects/" + str(object_id)
        response = self.get_response(endpoint).json()
        if response.ok:
            return response.json()
        else:
            return None
