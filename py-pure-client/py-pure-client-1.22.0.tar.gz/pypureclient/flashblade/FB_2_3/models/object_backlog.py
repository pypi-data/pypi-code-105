# coding: utf-8

"""
    FlashBlade REST API

    A lightweight client for FlashBlade REST API 2.3, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flashblade.FB_2_3 import models

class ObjectBacklog(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'bytes_count': 'int',
        'delete_ops_count': 'int',
        'other_ops_count': 'int',
        'put_ops_count': 'int'
    }

    attribute_map = {
        'bytes_count': 'bytes_count',
        'delete_ops_count': 'delete_ops_count',
        'other_ops_count': 'other_ops_count',
        'put_ops_count': 'put_ops_count'
    }

    required_args = {
    }

    def __init__(
        self,
        bytes_count=None,  # type: int
        delete_ops_count=None,  # type: int
        other_ops_count=None,  # type: int
        put_ops_count=None,  # type: int
    ):
        """
        Keyword args:
            bytes_count (int): The size of the objects in bytes that need to be replicated. This does not include the size of custom metadata.
            delete_ops_count (int): The number of DELETE operations that need to be replicated.
            other_ops_count (int): The number of other operations that need to be replicated.
            put_ops_count (int): The number of PUT operations that need to be replicated.
        """
        if bytes_count is not None:
            self.bytes_count = bytes_count
        if delete_ops_count is not None:
            self.delete_ops_count = delete_ops_count
        if other_ops_count is not None:
            self.other_ops_count = other_ops_count
        if put_ops_count is not None:
            self.put_ops_count = put_ops_count

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `ObjectBacklog`".format(key))
        self.__dict__[key] = value

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if isinstance(value, Property):
            return None
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
        if issubclass(ObjectBacklog, dict):
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
        if not isinstance(other, ObjectBacklog):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
