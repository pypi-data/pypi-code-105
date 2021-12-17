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

class Qos(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'bandwidth_limit': 'int',
        'iops_limit': 'int'
    }

    attribute_map = {
        'bandwidth_limit': 'bandwidth_limit',
        'iops_limit': 'iops_limit'
    }

    required_args = {
    }

    def __init__(
        self,
        bandwidth_limit=None,  # type: int
        iops_limit=None,  # type: int
    ):
        """
        Keyword args:
            bandwidth_limit (int): The maximum QoS bandwidth limit for the volume. Whenever throughput exceeds the bandwidth limit, throttling occurs. Measured in bytes per second. Maximum limit is 512 GB/s.
            iops_limit (int): The QoS IOPs limit for the volume.
        """
        if bandwidth_limit is not None:
            self.bandwidth_limit = bandwidth_limit
        if iops_limit is not None:
            self.iops_limit = iops_limit

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Qos`".format(key))
        if key == "bandwidth_limit" and value is not None:
            if value > 549755813888:
                raise ValueError("Invalid value for `bandwidth_limit`, value must be less than or equal to `549755813888`")
            if value < 1048576:
                raise ValueError("Invalid value for `bandwidth_limit`, must be a value greater than or equal to `1048576`")
        if key == "iops_limit" and value is not None:
            if value > 104857600:
                raise ValueError("Invalid value for `iops_limit`, value must be less than or equal to `104857600`")
            if value < 100:
                raise ValueError("Invalid value for `iops_limit`, must be a value greater than or equal to `100`")
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
        if issubclass(Qos, dict):
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
        if not isinstance(other, Qos):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
