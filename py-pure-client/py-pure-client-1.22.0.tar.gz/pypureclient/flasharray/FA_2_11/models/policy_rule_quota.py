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

class PolicyRuleQuota(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'enforced': 'bool',
        'name': 'str',
        'notifications': 'str',
        'policy': 'FixedReferenceWithType',
        'quota_limit': 'int'
    }

    attribute_map = {
        'enforced': 'enforced',
        'name': 'name',
        'notifications': 'notifications',
        'policy': 'policy',
        'quota_limit': 'quota_limit'
    }

    required_args = {
    }

    def __init__(
        self,
        enforced=None,  # type: bool
        name=None,  # type: str
        notifications=None,  # type: str
        policy=None,  # type: models.FixedReferenceWithType
        quota_limit=None,  # type: int
    ):
        """
        Keyword args:
            enforced (bool): Defines whether the quota rule is enforced or unenforced. If the quota rule is enforced and logical space usage exceeds the quota limit, any modification operations that result in a need for more space are blocked. If the quota rule is unenforced and logical space usage exceeds the quota limit, notification emails are sent to targets that are specified using the `notification` parameter. No client operations are blocked when an unenforced limit is exceeded. If set to `true`, the limit is enforced. If set to `false`, notification targets are informed when the usage exceeds 80 percent of the limit.
            name (str): Name of this rule. The name is automatically generated by the system.
            notifications (str): Targets to notify when usage approaches the quota limit. The list of notification targets is a comma-separated string. Valid values are `user`, and `group`. If not specified, notification targets are not assigned for the rule.
            policy (FixedReferenceWithType): The policy to which this rule belongs.
            quota_limit (int): Logical space limit of the quota assigned by the rule, measured in bytes. This value cannot be set to 0.
        """
        if enforced is not None:
            self.enforced = enforced
        if name is not None:
            self.name = name
        if notifications is not None:
            self.notifications = notifications
        if policy is not None:
            self.policy = policy
        if quota_limit is not None:
            self.quota_limit = quota_limit

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `PolicyRuleQuota`".format(key))
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
        if issubclass(PolicyRuleQuota, dict):
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
        if not isinstance(other, PolicyRuleQuota):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
