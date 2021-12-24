from typing import Any, List, Optional, Callable
from fastapi import UploadFile
import requests
from pydantic import BaseModel
import aiohttp
from abc import ABC, abstractmethod
import asyncio
import json
import urllib.request as url_request
import urllib.parse as url_parse


# model for settings
class GlobalCallSettings(BaseModel):
    """base model for settings calls"""
    protocol: Optional[str] = 'requests'
    reverse_model: Optional[str] = 'roof_top'
    density_model: Optional[str] = '2dSphere'


# utilities class
class Utilities:

    def __init__(self):
        self.name = 'util'

    @staticmethod
    def coords_conv(coordinates):
        """convert coordinates to lats and longs"""

        # create containers for lats and longs
        lats = []
        longs = []

        # separate the latitudes and longitudes
        [(lats.append(i[0]), longs.append(i[1])) for i in coordinates]

        return [lats, longs]


# implement strategy pattern for request call protocols
class ProtocolStrategy(ABC):
    """protocol abstract base class for strategy implementation"""

    @abstractmethod
    def call_protocol(self, response: Callable) -> Any:
        pass


class BasicRequest(ProtocolStrategy):
    """basic requests"""

    @abstractmethod
    def call_protocol(self, response: Callable) -> Any:
        return response()


# noinspection PyTypeChecker
class AIORequest(ProtocolStrategy):
    """run the asynchronous request for aiohttp protocol"""

    @abstractmethod
    def call_protocol(self, response: Callable) -> Any:
        return asyncio.run(response)


class URLLIBRequest(ProtocolStrategy):
    """urllib reader protocol processor"""

    @abstractmethod
    def call_protocol(self, response: Callable) -> Any:
        return json.loads(response())


class Places(Utilities):
    """places facade class for package contents"""

    def __init__(self, token: str):
        # get base model for global states
        super().__init__()
        self.global_model: GlobalCallSettings = GlobalCallSettings()

        # access token
        self.token: str = token

        # base url for places geocoding server
        self.url_mapping: dict = {1: f'https://places-api-dob9z.ondigitalocean.app/{self.global_model.reverse_model}',
                                  2: f'https://places-api-dob9z.ondigitalocean.app/{self.global_model.density_model}'}

        # create mapping for caller and protocols
        protocol_mapping: dict = {'request': (BasicRequest(), self._call_url_requests),
                                  'aiohttp': (AIORequest(), self._call_url_aiohttp),
                                  'urllib': (URLLIBRequest, self._call_url_urllib)}
        # unpack the strategies
        self.proto_runner, self.call_runner = protocol_mapping[self.global_model.protocol]

    @staticmethod
    def _unpack_runtime(runtime: dict):
        """unpack the runtime type"""
        # get the type of request to be made
        try:
            request_type: int = runtime['type']
        except KeyError:
            request_type: int = 1

        return request_type

    def _call_url_requests(self, payload: dict, **runtime):
        """call the url with requests library"""

        # get the type of request to be made
        request_type = self._unpack_runtime(runtime)

        # get the request in JSON
        return requests.get(self.url_mapping[request_type], params=payload).json()

    async def _call_url_aiohttp(self, payload: dict, **runtime):
        """call url with aiohttp library"""

        # get the type of request to be made
        request_type = self._unpack_runtime(runtime)

        # make asynchronous request
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_mapping[request_type], params=payload) as resp:
                response = await resp.json()

        return response

    def _call_url_urllib(self, payload: dict, **runtime):
        """urllib caller function"""

        # get the request type
        request_type = self._unpack_runtime(runtime)

        # encode the parameters
        query_string: str = url_parse.urlencode(payload)
        url: str = self.url_mapping[request_type] + "?" + query_string

        # make request to server
        with url_request.urlopen(url) as response:
            return response.read()

    @staticmethod
    def process_basic_args(additional_args: dict) -> bool:
        """process the basic arguments for load radius, convex, density, reverse, and batch reverse methods"""

        # reverse_parameter extraction
        try:
            reverse_param: Any = additional_args['reverse_param']
        except KeyError:
            reverse_param: Any = None

        return reverse_param

    def load_properties(self, coordinates: list = (), radius: Any = 10, **additional):
        """load properties facade for package purposes"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additional)
        payload: dict = {"coordinates": coordinates, "radius": radius, "token": self.token,
                         'reverse_param': reverse_param}

        # create and send response package
        return self.proto_runner.call_protocol(self.call_runner(payload, type=1))

    def convex(self, coordinates: list, **additionals) -> Any:
        """convex search facade method for places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)
        payload: dict = {"coordinates": coordinates, "reverse_param": reverse_param, "token": self.token}

        # create response and send it
        return self.proto_runner.call_protocol(self.call_runner(payload, type=1))

    def density(self, unit_in="ft", unit_out="ft", coordinate: list = None, radius: Any = 1,
                custom_option: str = None, custom_utility: Any = None, **additionals) -> Any:
        """density facade function for places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)
        payload: dict = {"token": self.token, "coordinate": coordinate, "unit_in": unit_in, "unit_out": unit_out,
                         "radius": radius, "reverse_param": reverse_param, "custom_option": custom_option,
                         "custom_utility": custom_utility}

        return self.proto_runner.call_protocol(self.call_runner(payload, type=2))

    def reverse(self, coordinate: list = (), radius: Any = 10, **additionals) -> Any:
        """reverse geocoding facade method for Places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)
        payload: dict = {"token": self.token, "coordinate": coordinate, "radius": radius,
                         "reverse_param": reverse_param}

        # create and send response packet
        return self.proto_runner.call_protocol(self.call_runner(payload, type=1))

    def batch_reverse(self, coordinates: List[list] = (()), radius: Any = 10, coordinate_file: UploadFile = None,
                      **additionals) -> Any:
        """batch reverse geocoding facade method for Places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)

        # create containers for lats and longs
        lats, longs = self.coords_conv(coordinates)

        # create request payload
        payload: dict = {"token": self.token, "latitudes": lats, "longitudes": longs, "radius": radius,
                         "coordinate_file": coordinate_file, "reverse_param": reverse_param}

        # create and send response packet
        return self.proto_runner.call_protocol(self.call_runner(payload, type=1))

    def forward(self, full_address: str = None, street: str = None, number: Any = None, postcode: int = None,
                region: str = None, city: str = None, unit=None) -> Any:
        """facade method for forward geocoding on Places API"""

        # create payload
        payload: dict = {"token": self.token, "full_address": full_address, "street": street, "number": number,
                         "postcode": postcode, "region": region, "city": city, "unit": unit}

        return self.proto_runner.call_protocol(self.call_runner(payload, type=1))

    def batch_forward(self, addresses: list = (), address_file: UploadFile = None) -> Any:
        """batch forward facade method"""

        # create request payload
        payload: dict = {"token": self.token, "addresses": addresses, "address_file": address_file}

        # create the send response
        return self.proto_runner.call_protocol(self.call_runner(payload, type=1))