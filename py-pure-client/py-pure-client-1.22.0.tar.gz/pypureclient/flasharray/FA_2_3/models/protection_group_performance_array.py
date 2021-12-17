# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_3 import models

class ProtectionGroupPerformanceArray(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'bytes_per_sec': 'int',
        'source': 'str',
        'target': 'str',
        'time': 'int'
    }

    attribute_map = {
        'name': 'name',
        'bytes_per_sec': 'bytes_per_sec',
        'source': 'source',
        'target': 'target',
        'time': 'time'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        bytes_per_sec=None,  # type: int
        source=None,  # type: str
        target=None,  # type: str
        time=None,  # type: int
    ):
        """
        Keyword args:
            name (str): A locally unique, system-generated name. The name cannot be modified.
            bytes_per_sec (int): The total number of bytes of replication data transmitted and received per second.
            source (str): The source array from where the data is replicated.
            target (str): The target to where the data is replicated.
            time (int): The time when the sample performance data was taken. Measured in milliseconds since the UNIX epoch.
        """
        if name is not None:
            self.name = name
        if bytes_per_sec is not None:
            self.bytes_per_sec = bytes_per_sec
        if source is not None:
            self.source = source
        if target is not None:
            self.target = target
        if time is not None:
            self.time = time

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `ProtectionGroupPerformanceArray`".format(key))
        if key == "bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_sec`, must be a value greater than or equal to `0`")
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
        if issubclass(ProtectionGroupPerformanceArray, dict):
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
        if not isinstance(other, ProtectionGroupPerformanceArray):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
