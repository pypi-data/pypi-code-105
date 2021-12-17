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

class DirectoryServiceManagement(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'user_login_attribute': 'str',
        'user_object_class': 'str'
    }

    attribute_map = {
        'user_login_attribute': 'user_login_attribute',
        'user_object_class': 'user_object_class'
    }

    required_args = {
    }

    def __init__(
        self,
        user_login_attribute=None,  # type: str
        user_object_class=None,  # type: str
    ):
        """
        Keyword args:
            user_login_attribute (str): User login attribute in the structure of the configured LDAP servers. Typically the attribute field that holds the user's unique login name. Defaults to `sAMAccountName` for Active Directory servers, or `uid` for all other directory server types. 
            user_object_class (str): Value of the object class for a management LDAP user. Defaults to `User` for Active Directory servers, `posixAccount` or `shadowAccount` for OpenLDAP servers dependent on the server's group type, or `person` for all other directory servers. 
        """
        if user_login_attribute is not None:
            self.user_login_attribute = user_login_attribute
        if user_object_class is not None:
            self.user_object_class = user_object_class

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `DirectoryServiceManagement`".format(key))
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
        if issubclass(DirectoryServiceManagement, dict):
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
        if not isinstance(other, DirectoryServiceManagement):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
