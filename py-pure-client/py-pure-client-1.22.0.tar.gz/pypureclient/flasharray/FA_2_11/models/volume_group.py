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

class VolumeGroup(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'name': 'str',
        'destroyed': 'bool',
        'qos': 'Qos',
        'priority_adjustment': 'PriorityAdjustment',
        'space': 'Space',
        'time_remaining': 'int',
        'volume_count': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'destroyed': 'destroyed',
        'qos': 'qos',
        'priority_adjustment': 'priority_adjustment',
        'space': 'space',
        'time_remaining': 'time_remaining',
        'volume_count': 'volume_count'
    }

    required_args = {
    }

    def __init__(
        self,
        id=None,  # type: str
        name=None,  # type: str
        destroyed=None,  # type: bool
        qos=None,  # type: models.Qos
        priority_adjustment=None,  # type: models.PriorityAdjustment
        space=None,  # type: models.Space
        time_remaining=None,  # type: int
        volume_count=None,  # type: int
    ):
        """
        Keyword args:
            id (str): A globally unique, system-generated ID. The ID cannot be modified and cannot refer to another resource.
            name (str): A user-specified name. The name must be locally unique and can be changed.
            destroyed (bool): Returns a value of `true` if the volume group has been destroyed and is pending eradication. Before the `time_remaining` period has elapsed, the destroyed volume group can be recovered by setting `destroyed=false`. After the `time_remaining` period has elapsed, the volume group is permanently eradicated and cannot be recovered.
            qos (Qos)
            priority_adjustment (PriorityAdjustment)
            space (Space)
            time_remaining (int): The amount of time left until the destroyed volume group is permanently eradicated, measured in milliseconds.
            volume_count (int): The number of volumes in the volume group.
        """
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if destroyed is not None:
            self.destroyed = destroyed
        if qos is not None:
            self.qos = qos
        if priority_adjustment is not None:
            self.priority_adjustment = priority_adjustment
        if space is not None:
            self.space = space
        if time_remaining is not None:
            self.time_remaining = time_remaining
        if volume_count is not None:
            self.volume_count = volume_count

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `VolumeGroup`".format(key))
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
        if issubclass(VolumeGroup, dict):
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
        if not isinstance(other, VolumeGroup):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
