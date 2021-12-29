from json.decoder import JSONDecodeError
from .client import Http


class Response(Http):
    """
    Formatted HTTP response and returned
    as dict object with the status code
    """
    def json_response(self):
        try:
            response_body = self.response.json()
        except JSONDecodeError as e:
            raise Exception(f"Unable to decode the HTTP response {e}")
        except Exception as e:
            raise Exception(f"Another exception was occurs {e}")

        if self.response.status_code == 200:
            print(response_body, self.response.status_code)
        else:
            print(None, self.response.status_code)
