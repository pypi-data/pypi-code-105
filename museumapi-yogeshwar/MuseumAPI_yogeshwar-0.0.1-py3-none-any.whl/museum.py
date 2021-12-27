import requests
import logging


logging.basicConfig(filename='loggingfile.log', level=logging.DEBUG,
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

        except (requests.ConnectionError, requests.Timeout, requests.ConnectTimeout) as rerror:
            logging.error("Error occured : " + str(rerror))
        except requests.HTTPError as herror:
            logging.error("Error occured : " + str(herror))
        except Exception as e:
            logging.error("Error occured : " + str(e))

        return response

    def get_objectids(self):
        """
        It will get all object ids from museum API
        :return : It will return object ids in a dictionary
        :keys: * total: int
            count of object ids
                * object ids: list
            list of object ids
        """
        endpoint = "objects"
        return self.get_response(endpoint).json()

    def get_object_for_ids(self, object_id):
        """
        It will get an object with specified object ids
        :param object_id: object_id of the object
        :return : Dictionary containing objects
        """

        endpoint = "objects/" + str(object_id)
        return self.get_response(endpoint).json()
