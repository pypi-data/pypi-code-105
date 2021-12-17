# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.10
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_10 import models

class SnmpV3Patch(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'auth_passphrase': 'str',
        'auth_protocol': 'str',
        'privacy_passphrase': 'str',
        'privacy_protocol': 'str',
        'user': 'str'
    }

    attribute_map = {
        'auth_passphrase': 'auth_passphrase',
        'auth_protocol': 'auth_protocol',
        'privacy_passphrase': 'privacy_passphrase',
        'privacy_protocol': 'privacy_protocol',
        'user': 'user'
    }

    required_args = {
    }

    def __init__(
        self,
        auth_passphrase=None,  # type: str
        auth_protocol=None,  # type: str
        privacy_passphrase=None,  # type: str
        privacy_protocol=None,  # type: str
        user=None,  # type: str
    ):
        """
        Keyword args:
            auth_passphrase (str): Passphrase used by Purity//FA to authenticate the array with the specified managers.
            auth_protocol (str): Hash algorithm used to validate the authentication passphrase. Valid values are `MD5` and `SHA`.
            privacy_passphrase (str): Passphrase used to encrypt SNMP messages.
            privacy_protocol (str): Encryption protocol for SNMP messages. Valid values are `AES` and `DES`.
            user (str): User ID recognized by the specified SNMP managers which Purity//FA is to use in communications with them.
        """
        if auth_passphrase is not None:
            self.auth_passphrase = auth_passphrase
        if auth_protocol is not None:
            self.auth_protocol = auth_protocol
        if privacy_passphrase is not None:
            self.privacy_passphrase = privacy_passphrase
        if privacy_protocol is not None:
            self.privacy_protocol = privacy_protocol
        if user is not None:
            self.user = user

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `SnmpV3Patch`".format(key))
        if key == "auth_passphrase" and value is not None:
            if len(value) > 32:
                raise ValueError("Invalid value for `auth_passphrase`, length must be less than or equal to `32`")
        if key == "privacy_passphrase" and value is not None:
            if len(value) > 63:
                raise ValueError("Invalid value for `privacy_passphrase`, length must be less than or equal to `63`")
            if len(value) < 8:
                raise ValueError("Invalid value for `privacy_passphrase`, length must be greater than or equal to `8`")
        self.__dict__[key] = value

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if isinstance(value, Property):
            raise AttributeError
        else:
            return value

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            if hasattr(self, attr):
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
        if issubclass(SnmpV3Patch, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SnmpV3Patch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
