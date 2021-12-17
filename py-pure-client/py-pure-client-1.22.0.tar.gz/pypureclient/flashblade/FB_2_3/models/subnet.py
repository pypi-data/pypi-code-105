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

class Subnet(object):
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
        'enabled': 'bool',
        'gateway': 'str',
        'interfaces': 'list[FixedReference]',
        'link_aggregation_group': 'Reference',
        'mtu': 'int',
        'prefix': 'str',
        'services': 'list[str]',
        'vlan': 'int'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'enabled': 'enabled',
        'gateway': 'gateway',
        'interfaces': 'interfaces',
        'link_aggregation_group': 'link_aggregation_group',
        'mtu': 'mtu',
        'prefix': 'prefix',
        'services': 'services',
        'vlan': 'vlan'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        id=None,  # type: str
        enabled=None,  # type: bool
        gateway=None,  # type: str
        interfaces=None,  # type: List[models.FixedReference]
        link_aggregation_group=None,  # type: models.Reference
        mtu=None,  # type: int
        prefix=None,  # type: str
        services=None,  # type: List[str]
        vlan=None,  # type: int
    ):
        """
        Keyword args:
            name (str): Name of the object (e.g., a file system or snapshot).
            id (str): A non-modifiable, globally unique ID chosen by the system.
            enabled (bool): Indicates if subnet is enabled (`true`) or disabled (`false`). If not specified, defaults to `true`.
            gateway (str): The IPv4 or IPv6 address of the gateway through which the specified subnet is to communicate with the network.
            interfaces (list[FixedReference]): List of network interfaces associated with this subnet.
            link_aggregation_group (Reference): Reference to the associated LAG.
            mtu (int): Maximum message transfer unit (packet) size for the subnet in bytes. MTU setting cannot exceed the MTU of the corresponding physical interface. If not specified, defaults to `1500`.
            prefix (str): The IPv4 or IPv6 address to be associated with the specified subnet.
            services (list[str]): The services provided by this subnet, as inherited from all of its interfaces.
            vlan (int): VLAN ID.
        """
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if enabled is not None:
            self.enabled = enabled
        if gateway is not None:
            self.gateway = gateway
        if interfaces is not None:
            self.interfaces = interfaces
        if link_aggregation_group is not None:
            self.link_aggregation_group = link_aggregation_group
        if mtu is not None:
            self.mtu = mtu
        if prefix is not None:
            self.prefix = prefix
        if services is not None:
            self.services = services
        if vlan is not None:
            self.vlan = vlan

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Subnet`".format(key))
        if key == "mtu" and value is not None:
            if value > 9216:
                raise ValueError("Invalid value for `mtu`, value must be less than or equal to `9216`")
            if value < 1280:
                raise ValueError("Invalid value for `mtu`, must be a value greater than or equal to `1280`")
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
        if issubclass(Subnet, dict):
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
        if not isinstance(other, Subnet):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
