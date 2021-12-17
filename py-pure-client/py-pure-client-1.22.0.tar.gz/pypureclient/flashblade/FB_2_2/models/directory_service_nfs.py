# coding: utf-8

"""
    FlashBlade REST API

    A lightweight client for FlashBlade REST API 2.2, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flashblade.FB_2_2 import models

class DirectoryServiceNfs(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'nis_domains': 'list[str]',
        'nis_servers': 'list[str]'
    }

    attribute_map = {
        'nis_domains': 'nis_domains',
        'nis_servers': 'nis_servers'
    }

    required_args = {
    }

    def __init__(
        self,
        nis_domains=None,  # type: List[str]
        nis_servers=None,  # type: List[str]
    ):
        """
        Keyword args:
            nis_domains (list[str]): NIS domains to search.
            nis_servers (list[str]): A list of the IP addresses or hostnames of NIS servers to search.
        """
        if nis_domains is not None:
            self.nis_domains = nis_domains
        if nis_servers is not None:
            self.nis_servers = nis_servers

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `DirectoryServiceNfs`".format(key))
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
        if issubclass(DirectoryServiceNfs, dict):
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
        if not isinstance(other, DirectoryServiceNfs):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
