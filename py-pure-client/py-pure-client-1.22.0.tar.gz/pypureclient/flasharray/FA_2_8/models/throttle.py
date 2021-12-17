# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.8
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_8 import models

class Throttle(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'default_limit': 'int',
        'window': 'TimeWindow',
        'window_limit': 'int'
    }

    attribute_map = {
        'default_limit': 'default_limit',
        'window': 'window',
        'window_limit': 'window_limit'
    }

    required_args = {
    }

    def __init__(
        self,
        default_limit=None,  # type: int
        window=None,  # type: models.TimeWindow
        window_limit=None,  # type: int
    ):
        """
        Keyword args:
            default_limit (int): Default maximum bandwidth threshold for outbound traffic in bytes. Once exceeded, bandwidth throttling occurs.
            window (TimeWindow): The time during which the `window_limit` threshold is in effect.
            window_limit (int): Maximum bandwidth threshold for outbound traffic during the specified `window_limit` time range in bytes. Once exceeded, bandwidth throttling occurs.
        """
        if default_limit is not None:
            self.default_limit = default_limit
        if window is not None:
            self.window = window
        if window_limit is not None:
            self.window_limit = window_limit

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Throttle`".format(key))
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
        if issubclass(Throttle, dict):
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
        if not isinstance(other, Throttle):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
