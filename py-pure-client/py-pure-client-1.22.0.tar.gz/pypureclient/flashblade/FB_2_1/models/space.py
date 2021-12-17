# coding: utf-8

"""
    FlashBlade REST API

    A lightweight client for FlashBlade REST API 2.1, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flashblade.FB_2_1 import models

class Space(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'data_reduction': 'float',
        'snapshots': 'int',
        'total_physical': 'int',
        'unique': 'int',
        'virtual': 'int'
    }

    attribute_map = {
        'data_reduction': 'data_reduction',
        'snapshots': 'snapshots',
        'total_physical': 'total_physical',
        'unique': 'unique',
        'virtual': 'virtual'
    }

    required_args = {
    }

    def __init__(
        self,
        data_reduction=None,  # type: float
        snapshots=None,  # type: int
        total_physical=None,  # type: int
        unique=None,  # type: int
        virtual=None,  # type: int
    ):
        """
        Keyword args:
            data_reduction (float): Reduction of data.
            snapshots (int): Physical usage by snapshots, other than unique in bytes.
            total_physical (int): Total physical usage (including snapshots) in bytes.
            unique (int): Unique physical space occupied by customer data, in bytes. Excludes shared space, snapshots, and metadata.
            virtual (int): Virtual space, in bytes.
        """
        if data_reduction is not None:
            self.data_reduction = data_reduction
        if snapshots is not None:
            self.snapshots = snapshots
        if total_physical is not None:
            self.total_physical = total_physical
        if unique is not None:
            self.unique = unique
        if virtual is not None:
            self.virtual = virtual

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Space`".format(key))
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
        if issubclass(Space, dict):
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
        if not isinstance(other, Space):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
