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


class AddressRequired(object):
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
        'phone': 'str',
        'country': 'str',
        'zip': 'str'
    }

    attribute_map = {
        'phone': 'phone',
        'country': 'country',
        'zip': 'zip'
    }

    def __init__(self, phone=None, country=None, zip=None, local_vars_configuration=None):  # noqa: E501
        """AddressRequired - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._phone = None
        self._country = None
        self._zip = None
        self.discriminator = None

        self.phone = phone
        self.country = country
        self.zip = zip

    @property
    def phone(self):
        """Gets the phone of this AddressRequired.  # noqa: E501

        The phone of customer  # noqa: E501

        :return: The phone of this AddressRequired.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this AddressRequired.

        The phone of customer  # noqa: E501

        :param phone: The phone of this AddressRequired.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and phone is None:  # noqa: E501
            raise ValueError("Invalid value for `phone`, must not be `None`")  # noqa: E501

        self._phone = phone

    @property
    def country(self):
        """Gets the country of this AddressRequired.  # noqa: E501


        :return: The country of this AddressRequired.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this AddressRequired.


        :param country: The country of this AddressRequired.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and country is None:  # noqa: E501
            raise ValueError("Invalid value for `country`, must not be `None`")  # noqa: E501

        self._country = country

    @property
    def zip(self):
        """Gets the zip of this AddressRequired.  # noqa: E501

        Postal Code / Zip, please set to . if not known  # noqa: E501

        :return: The zip of this AddressRequired.  # noqa: E501
        :rtype: str
        """
        return self._zip

    @zip.setter
    def zip(self, zip):
        """Sets the zip of this AddressRequired.

        Postal Code / Zip, please set to . if not known  # noqa: E501

        :param zip: The zip of this AddressRequired.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and zip is None:  # noqa: E501
            raise ValueError("Invalid value for `zip`, must not be `None`")  # noqa: E501

        self._zip = zip

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
        if not isinstance(other, AddressRequired):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddressRequired):
            return True

        return self.to_dict() != other.to_dict()
