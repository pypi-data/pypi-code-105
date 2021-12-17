# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.6
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_6 import models

class VolumeCommon(object):
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
        'connection_count': 'int',
        'created': 'int',
        'destroyed': 'bool',
        'host_encryption_key_status': 'str',
        'provisioned': 'int',
        'qos': 'Qos',
        'serial': 'str',
        'space': 'Space',
        'time_remaining': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'connection_count': 'connection_count',
        'created': 'created',
        'destroyed': 'destroyed',
        'host_encryption_key_status': 'host_encryption_key_status',
        'provisioned': 'provisioned',
        'qos': 'qos',
        'serial': 'serial',
        'space': 'space',
        'time_remaining': 'time_remaining'
    }

    required_args = {
    }

    def __init__(
        self,
        id=None,  # type: str
        name=None,  # type: str
        connection_count=None,  # type: int
        created=None,  # type: int
        destroyed=None,  # type: bool
        host_encryption_key_status=None,  # type: str
        provisioned=None,  # type: int
        qos=None,  # type: models.Qos
        serial=None,  # type: str
        space=None,  # type: models.Space
        time_remaining=None,  # type: int
    ):
        """
        Keyword args:
            id (str): A globally unique, system-generated ID. The ID cannot be modified and cannot refer to another resource.
            name (str): A user-specified name. The name must be locally unique and can be changed.
            connection_count (int): The total number of hosts and host groups connected to the volume.
            created (int): The volume creation time. Measured in milliseconds since the UNIX epoch.
            destroyed (bool): Returns a value of `true` if the volume has been destroyed and is pending eradication. The `time_remaining` value displays the amount of time left until the destroyed volume is permanently eradicated. Before the `time_remaining` period has elapsed, the destroyed volume can be recovered by setting `destroyed=false`. Once the `time_remaining` period has elapsed, the volume is permanently eradicated and can no longer be recovered.
            host_encryption_key_status (str): The host encryption key status for this volume. Possible values include `none`, `detected`, and `fetched`.
            provisioned (int): The virtual size of the volume. Measured in bytes and must be a multiple of 512.
            qos (Qos): Displays QoS limit information.
            serial (str): A globally unique serial number generated by the system when the volume is created.
            space (Space): Displays size and space consumption information.
            time_remaining (int): The amount of time left until the destroyed volume is permanently eradicated. Measured in milliseconds. Before the `time_remaining` period has elapsed, the destroyed volume can be recovered by setting `destroyed=false`.
        """
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if connection_count is not None:
            self.connection_count = connection_count
        if created is not None:
            self.created = created
        if destroyed is not None:
            self.destroyed = destroyed
        if host_encryption_key_status is not None:
            self.host_encryption_key_status = host_encryption_key_status
        if provisioned is not None:
            self.provisioned = provisioned
        if qos is not None:
            self.qos = qos
        if serial is not None:
            self.serial = serial
        if space is not None:
            self.space = space
        if time_remaining is not None:
            self.time_remaining = time_remaining

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `VolumeCommon`".format(key))
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
        if issubclass(VolumeCommon, dict):
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
        if not isinstance(other, VolumeCommon):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
