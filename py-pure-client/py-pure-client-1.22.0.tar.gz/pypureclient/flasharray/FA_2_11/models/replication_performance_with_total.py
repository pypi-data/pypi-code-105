# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.11
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_11 import models

class ReplicationPerformanceWithTotal(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'from_remote_bytes_per_sec': 'int',
        'to_remote_bytes_per_sec': 'int',
        'total_bytes_per_sec': 'int'
    }

    attribute_map = {
        'from_remote_bytes_per_sec': 'from_remote_bytes_per_sec',
        'to_remote_bytes_per_sec': 'to_remote_bytes_per_sec',
        'total_bytes_per_sec': 'total_bytes_per_sec'
    }

    required_args = {
    }

    def __init__(
        self,
        from_remote_bytes_per_sec=None,  # type: int
        to_remote_bytes_per_sec=None,  # type: int
        total_bytes_per_sec=None,  # type: int
    ):
        """
        Keyword args:
            from_remote_bytes_per_sec (int): The number of bytes received per second from a remote array. The number will be zero if the arrays are unable to communicate.
            to_remote_bytes_per_sec (int): The number of bytes transmitted per second to a remote array. The number will be zero if the arrays are unable to communicate.
            total_bytes_per_sec (int): Total bytes transmitted and received per second. The number will be zero if the arrays are unable to communicate.
        """
        if from_remote_bytes_per_sec is not None:
            self.from_remote_bytes_per_sec = from_remote_bytes_per_sec
        if to_remote_bytes_per_sec is not None:
            self.to_remote_bytes_per_sec = to_remote_bytes_per_sec
        if total_bytes_per_sec is not None:
            self.total_bytes_per_sec = total_bytes_per_sec

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `ReplicationPerformanceWithTotal`".format(key))
        if key == "from_remote_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `from_remote_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "to_remote_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `to_remote_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "total_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `total_bytes_per_sec`, must be a value greater than or equal to `0`")
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
        if issubclass(ReplicationPerformanceWithTotal, dict):
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
        if not isinstance(other, ReplicationPerformanceWithTotal):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
