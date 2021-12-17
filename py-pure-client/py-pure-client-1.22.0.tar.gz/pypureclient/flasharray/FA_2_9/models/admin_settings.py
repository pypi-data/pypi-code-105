# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.9
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_9 import models

class AdminSettings(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'lockout_duration': 'int',
        'max_login_attempts': 'int',
        'min_password_length': 'int',
        'single_sign_on_enabled': 'bool'
    }

    attribute_map = {
        'lockout_duration': 'lockout_duration',
        'max_login_attempts': 'max_login_attempts',
        'min_password_length': 'min_password_length',
        'single_sign_on_enabled': 'single_sign_on_enabled'
    }

    required_args = {
    }

    def __init__(
        self,
        lockout_duration=None,  # type: int
        max_login_attempts=None,  # type: int
        min_password_length=None,  # type: int
        single_sign_on_enabled=None,  # type: bool
    ):
        """
        Keyword args:
            lockout_duration (int): The lockout duration, in milliseconds, if a user is locked out after reaching the maximum number of login attempts. Ranges from 1 second to 90 days.
            max_login_attempts (int): Maximum number of failed login attempts allowed before the user is locked out.
            min_password_length (int): Minimum password length. If not specified, defaults to 1.
            single_sign_on_enabled (bool): If `true`, then single sign-on is enabled for the array.
        """
        if lockout_duration is not None:
            self.lockout_duration = lockout_duration
        if max_login_attempts is not None:
            self.max_login_attempts = max_login_attempts
        if min_password_length is not None:
            self.min_password_length = min_password_length
        if single_sign_on_enabled is not None:
            self.single_sign_on_enabled = single_sign_on_enabled

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `AdminSettings`".format(key))
        if key == "lockout_duration" and value is not None:
            if value > 7776000000:
                raise ValueError("Invalid value for `lockout_duration`, value must be less than or equal to `7776000000`")
            if value < 1000:
                raise ValueError("Invalid value for `lockout_duration`, must be a value greater than or equal to `1000`")
        if key == "max_login_attempts" and value is not None:
            if value > 20:
                raise ValueError("Invalid value for `max_login_attempts`, value must be less than or equal to `20`")
            if value < 1:
                raise ValueError("Invalid value for `max_login_attempts`, must be a value greater than or equal to `1`")
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
        if issubclass(AdminSettings, dict):
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
        if not isinstance(other, AdminSettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
