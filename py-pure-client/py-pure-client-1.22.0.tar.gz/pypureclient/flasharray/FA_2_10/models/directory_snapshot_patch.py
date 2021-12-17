# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.10
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_10 import models

class DirectorySnapshotPatch(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'destroyed': 'bool',
        'keep_for': 'int',
        'policy': 'Reference',
        'name': 'str',
        'client_name': 'str',
        'suffix': 'str'
    }

    attribute_map = {
        'destroyed': 'destroyed',
        'keep_for': 'keep_for',
        'policy': 'policy',
        'name': 'name',
        'client_name': 'client_name',
        'suffix': 'suffix'
    }

    required_args = {
    }

    def __init__(
        self,
        destroyed=None,  # type: bool
        keep_for=None,  # type: int
        policy=None,  # type: models.Reference
        name=None,  # type: str
        client_name=None,  # type: str
        suffix=None,  # type: str
    ):
        """
        Keyword args:
            destroyed (bool): If set to `true`, destroys a resource. Once set to `true`, the `time_remaining` value will display the amount of time left until the destroyed resource is permanently eradicated. Before the `time_remaining` period has elapsed, the destroyed resource can be recovered by setting `destroyed=false`. Once the `time_remaining` period has elapsed, the resource is permanently eradicated and can no longer be recovered.
            keep_for (int): The amount of time to keep the snapshots, in milliseconds. Can only be set on snapshots that are not managed by any snapshot policy. Set to `\"\"` to clear the keep_for value.
            policy (Reference): The snapshot policy that manages this snapshot. Set to `name` or `id` to `\"\"` to clear the policy.
            name (str): The new name of a directory snapshot. The name of a directory snapshot managed by a snapshot policy is not changeable.
            client_name (str): The client name portion of the client-visible snapshot name. A full snapshot name is constructed in the form of `DIR.CLIENT_NAME.SUFFIX` where `DIR` is the managed directory name, `CLIENT_NAME` is the value of this field, and `SUFFIX` is the suffix. The client-visible snapshot name is `CLIENT_NAME.SUFFIX`. The client name of a directory snapshot managed by a snapshot policy is not changeable. If the `name` and `client_name` parameters are both specified, `client_name` must match the client name portion of `name`.
            suffix (str): The suffix portion of the client-visible snapshot name. A full snapshot name is constructed in the form of `DIR.CLIENT_NAME.SUFFIX` where `DIR` is the managed directory name, `CLIENT_NAME` is the client name, and `SUFFIX` is the value of this field. The client-visible snapshot name is `CLIENT_NAME.SUFFIX`. The suffix of a directory snapshot managed by a snapshot policy is not changeable. If the `name` and `suffix` parameters are both specified, `suffix` must match the suffix portion of `name`.
        """
        if destroyed is not None:
            self.destroyed = destroyed
        if keep_for is not None:
            self.keep_for = keep_for
        if policy is not None:
            self.policy = policy
        if name is not None:
            self.name = name
        if client_name is not None:
            self.client_name = client_name
        if suffix is not None:
            self.suffix = suffix

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `DirectorySnapshotPatch`".format(key))
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
        if issubclass(DirectorySnapshotPatch, dict):
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
        if not isinstance(other, DirectorySnapshotPatch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
