# coding: utf-8

"""
    Nomad Pilot

    This is the API descriptor for the Nomad Pilot API, responsible for shipping and logistics processing. Developed by [Samarkand Global](https://www.samarkand.global/) in partnership with [SF Express](https://www.sf-express.com/), [eSinotrans](http://air.esinotrans.com/), [sto](http://sto-express.co.uk/). Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_pilot_cli` - Install for python with `pip install nomad-pilot-cli` - Install for Maven users `groupId, com.gitlab.samarkand-nomad; artifactId, nomad-pilot-cli`  # noqa: E501

    The version of the OpenAPI document: 1.44.21
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from nomad_pilot_cli.configuration import Configuration


class ApiResponseConnectorResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'input': 'str',
        'mapping_name': 'str',
        'api': 'list[str]',
        'http_request_raw_data': 'str',
        'code': 'int',
        'response': 'str',
        'response_en': 'str',
        'platform': 'str',
        'request_count': 'int',
        'response_time': 'int'
    }

    attribute_map = {
        'input': 'input',
        'mapping_name': 'mappingName',
        'api': 'api',
        'http_request_raw_data': 'httpRequestRawData',
        'code': 'code',
        'response': 'response',
        'response_en': 'responseEn',
        'platform': 'platform',
        'request_count': 'requestCount',
        'response_time': 'responseTime'
    }

    def __init__(self, input=None, mapping_name=None, api=None, http_request_raw_data=None, code=None, response=None, response_en=None, platform=None, request_count=None, response_time=None, local_vars_configuration=None):  # noqa: E501
        """ApiResponseConnectorResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._input = None
        self._mapping_name = None
        self._api = None
        self._http_request_raw_data = None
        self._code = None
        self._response = None
        self._response_en = None
        self._platform = None
        self._request_count = None
        self._response_time = None
        self.discriminator = None

        if input is not None:
            self.input = input
        if mapping_name is not None:
            self.mapping_name = mapping_name
        if api is not None:
            self.api = api
        if http_request_raw_data is not None:
            self.http_request_raw_data = http_request_raw_data
        if code is not None:
            self.code = code
        if response is not None:
            self.response = response
        if response_en is not None:
            self.response_en = response_en
        if platform is not None:
            self.platform = platform
        if request_count is not None:
            self.request_count = request_count
        if response_time is not None:
            self.response_time = response_time

    @property
    def input(self):
        """Gets the input of this ApiResponseConnectorResponse.  # noqa: E501

        The input of a NomadOperation, usually it's JSON format.  # noqa: E501

        :return: The input of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: str
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this ApiResponseConnectorResponse.

        The input of a NomadOperation, usually it's JSON format.  # noqa: E501

        :param input: The input of this ApiResponseConnectorResponse.  # noqa: E501
        :type: str
        """

        self._input = input

    @property
    def mapping_name(self):
        """Gets the mapping_name of this ApiResponseConnectorResponse.  # noqa: E501

        The name of mapping class.  # noqa: E501

        :return: The mapping_name of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: str
        """
        return self._mapping_name

    @mapping_name.setter
    def mapping_name(self, mapping_name):
        """Sets the mapping_name of this ApiResponseConnectorResponse.

        The name of mapping class.  # noqa: E501

        :param mapping_name: The mapping_name of this ApiResponseConnectorResponse.  # noqa: E501
        :type: str
        """

        self._mapping_name = mapping_name

    @property
    def api(self):
        """Gets the api of this ApiResponseConnectorResponse.  # noqa: E501


        :return: The api of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._api

    @api.setter
    def api(self, api):
        """Sets the api of this ApiResponseConnectorResponse.


        :param api: The api of this ApiResponseConnectorResponse.  # noqa: E501
        :type: list[str]
        """

        self._api = api

    @property
    def http_request_raw_data(self):
        """Gets the http_request_raw_data of this ApiResponseConnectorResponse.  # noqa: E501

        Raw data of current HTTP request to the third party server, easy for debug.  # noqa: E501

        :return: The http_request_raw_data of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: str
        """
        return self._http_request_raw_data

    @http_request_raw_data.setter
    def http_request_raw_data(self, http_request_raw_data):
        """Sets the http_request_raw_data of this ApiResponseConnectorResponse.

        Raw data of current HTTP request to the third party server, easy for debug.  # noqa: E501

        :param http_request_raw_data: The http_request_raw_data of this ApiResponseConnectorResponse.  # noqa: E501
        :type: str
        """

        self._http_request_raw_data = http_request_raw_data

    @property
    def code(self):
        """Gets the code of this ApiResponseConnectorResponse.  # noqa: E501


        :return: The code of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this ApiResponseConnectorResponse.


        :param code: The code of this ApiResponseConnectorResponse.  # noqa: E501
        :type: int
        """

        self._code = code

    @property
    def response(self):
        """Gets the response of this ApiResponseConnectorResponse.  # noqa: E501


        :return: The response of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: str
        """
        return self._response

    @response.setter
    def response(self, response):
        """Sets the response of this ApiResponseConnectorResponse.


        :param response: The response of this ApiResponseConnectorResponse.  # noqa: E501
        :type: str
        """

        self._response = response

    @property
    def response_en(self):
        """Gets the response_en of this ApiResponseConnectorResponse.  # noqa: E501


        :return: The response_en of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: str
        """
        return self._response_en

    @response_en.setter
    def response_en(self, response_en):
        """Sets the response_en of this ApiResponseConnectorResponse.


        :param response_en: The response_en of this ApiResponseConnectorResponse.  # noqa: E501
        :type: str
        """

        self._response_en = response_en

    @property
    def platform(self):
        """Gets the platform of this ApiResponseConnectorResponse.  # noqa: E501


        :return: The platform of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this ApiResponseConnectorResponse.


        :param platform: The platform of this ApiResponseConnectorResponse.  # noqa: E501
        :type: str
        """

        self._platform = platform

    @property
    def request_count(self):
        """Gets the request_count of this ApiResponseConnectorResponse.  # noqa: E501

        The number of requests against the third party in one Nomad request.  # noqa: E501

        :return: The request_count of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: int
        """
        return self._request_count

    @request_count.setter
    def request_count(self, request_count):
        """Sets the request_count of this ApiResponseConnectorResponse.

        The number of requests against the third party in one Nomad request.  # noqa: E501

        :param request_count: The request_count of this ApiResponseConnectorResponse.  # noqa: E501
        :type: int
        """

        self._request_count = request_count

    @property
    def response_time(self):
        """Gets the response_time of this ApiResponseConnectorResponse.  # noqa: E501

        The response time of current NomadOperation request, including sub-NomadOperation. The time unit is millisecond.  # noqa: E501

        :return: The response_time of this ApiResponseConnectorResponse.  # noqa: E501
        :rtype: int
        """
        return self._response_time

    @response_time.setter
    def response_time(self, response_time):
        """Sets the response_time of this ApiResponseConnectorResponse.

        The response time of current NomadOperation request, including sub-NomadOperation. The time unit is millisecond.  # noqa: E501

        :param response_time: The response_time of this ApiResponseConnectorResponse.  # noqa: E501
        :type: int
        """

        self._response_time = response_time

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiResponseConnectorResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApiResponseConnectorResponse):
            return True

        return self.to_dict() != other.to_dict()
