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

class LinkAggregationGroup(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'id': 'str',
        'lag_speed': 'int',
        'mac_address': 'str',
        'ports': 'list[FixedReference]',
        'port_speed': 'int',
        'status': 'str'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'lag_speed': 'lag_speed',
        'mac_address': 'mac_address',
        'ports': 'ports',
        'port_speed': 'port_speed',
        'status': 'status'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        id=None,  # type: str
        lag_speed=None,  # type: int
        mac_address=None,  # type: str
        ports=None,  # type: List[models.FixedReference]
        port_speed=None,  # type: int
        status=None,  # type: str
    ):
        """
        Keyword args:
            name (str): Name of the object (e.g., a file system or snapshot).
            id (str): A non-modifiable, globally unique ID chosen by the system.
            lag_speed (int): Combined speed of all ports in the LAG in bits-per-second.
            mac_address (str): Unique MAC address assigned to the LAG.
            ports (list[FixedReference]): Ports associated with the LAG.
            port_speed (int): Configured speed of each port in the LAG in bits-per-second.
            status (str): Health status of the LAG. Valid values are `critical`, `healthy`, `identifying`, `unclaimed`, `unhealthy`, `unrecognized`, and `unused`.
        """
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if lag_speed is not None:
            self.lag_speed = lag_speed
        if mac_address is not None:
            self.mac_address = mac_address
        if ports is not None:
            self.ports = ports
        if port_speed is not None:
            self.port_speed = port_speed
        if status is not None:
            self.status = status

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `LinkAggregationGroup`".format(key))
        if key == "mac_address" and value is not None:
            if not re.search(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', value):
                raise ValueError(r"Invalid value for `mac_address`, must be a follow pattern or equal to `/^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/`")
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
        if issubclass(LinkAggregationGroup, dict):
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
        if not isinstance(other, LinkAggregationGroup):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
