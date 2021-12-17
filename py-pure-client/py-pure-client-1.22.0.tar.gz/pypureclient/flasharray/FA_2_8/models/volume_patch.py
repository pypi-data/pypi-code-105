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

class VolumePatch(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'destroyed': 'bool',
        'name': 'str',
        'pod': 'Reference',
        'provisioned': 'int',
        'qos': 'Qos',
        'volume_group': 'Reference',
        'requested_promotion_state': 'str'
    }

    attribute_map = {
        'destroyed': 'destroyed',
        'name': 'name',
        'pod': 'pod',
        'provisioned': 'provisioned',
        'qos': 'qos',
        'volume_group': 'volume_group',
        'requested_promotion_state': 'requested_promotion_state'
    }

    required_args = {
    }

    def __init__(
        self,
        destroyed=None,  # type: bool
        name=None,  # type: str
        pod=None,  # type: models.Reference
        provisioned=None,  # type: int
        qos=None,  # type: models.Qos
        volume_group=None,  # type: models.Reference
        requested_promotion_state=None,  # type: str
    ):
        """
        Keyword args:
            destroyed (bool): If set to `true`, destroys a resource. Once set to `true`, the `time_remaining` value will display the amount of time left until the destroyed resource is permanently eradicated. Before the `time_remaining` period has elapsed, the destroyed resource can be recovered by setting `destroyed=false`. Once the `time_remaining` period has elapsed, the resource is permanently eradicated and can no longer be recovered.
            name (str): The new name for the resource.
            pod (Reference): Moves the volume into the specified pod.
            provisioned (int): Updates the virtual size of the volume. Measured in bytes.
            qos (Qos): Sets QoS limits.
            volume_group (Reference): Adds the volume to the specified volume group.
            requested_promotion_state (str): Valid values are `promoted` and `demoted`. Patch `requested_promotion_state` to `demoted` to demote the volume so that the volume stops accepting write requests. Patch `requested_promotion_state` to `promoted` to promote the volume so that the volume starts accepting write requests.
        """
        if destroyed is not None:
            self.destroyed = destroyed
        if name is not None:
            self.name = name
        if pod is not None:
            self.pod = pod
        if provisioned is not None:
            self.provisioned = provisioned
        if qos is not None:
            self.qos = qos
        if volume_group is not None:
            self.volume_group = volume_group
        if requested_promotion_state is not None:
            self.requested_promotion_state = requested_promotion_state

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `VolumePatch`".format(key))
        if key == "provisioned" and value is not None:
            if value > 4503599627370496:
                raise ValueError("Invalid value for `provisioned`, value must be less than or equal to `4503599627370496`")
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
        if issubclass(VolumePatch, dict):
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
        if not isinstance(other, VolumePatch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
