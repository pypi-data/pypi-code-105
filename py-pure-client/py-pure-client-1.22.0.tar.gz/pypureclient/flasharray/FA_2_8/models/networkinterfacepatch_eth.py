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

class NetworkinterfacepatchEth(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'add_subinterfaces': 'list[FixedReferenceNoId]',
        'address': 'str',
        'gateway': 'str',
        'mtu': 'int',
        'netmask': 'str',
        'remove_subinterfaces': 'list[FixedReferenceNoId]',
        'subinterfaces': 'list[FixedReferenceNoId]',
        'subnet': 'ReferenceNoId'
    }

    attribute_map = {
        'add_subinterfaces': 'add_subinterfaces',
        'address': 'address',
        'gateway': 'gateway',
        'mtu': 'mtu',
        'netmask': 'netmask',
        'remove_subinterfaces': 'remove_subinterfaces',
        'subinterfaces': 'subinterfaces',
        'subnet': 'subnet'
    }

    required_args = {
    }

    def __init__(
        self,
        add_subinterfaces=None,  # type: List[models.FixedReferenceNoId]
        address=None,  # type: str
        gateway=None,  # type: str
        mtu=None,  # type: int
        netmask=None,  # type: str
        remove_subinterfaces=None,  # type: List[models.FixedReferenceNoId]
        subinterfaces=None,  # type: List[models.FixedReferenceNoId]
        subnet=None,  # type: models.ReferenceNoId
    ):
        """
        Keyword args:
            add_subinterfaces (list[FixedReferenceNoId]): Child devices to be added to the specified bond interface.
            address (str): The IPv4 or IPv6 address to be associated with the specified network interface.
            gateway (str): The IPv4 or IPv6 address of the gateway through which the specified network interface is to communicate with the network.
            mtu (int): Maximum message transfer unit (packet) size for the network interface in bytes. MTU setting cannot exceed the MTU of the corresponding physical interface.
            netmask (str): Netmask of the specified network interface that, when combined with the address of the interface, determines the network address of the interface.
            remove_subinterfaces (list[FixedReferenceNoId]): Child devices to be removed from the specified bond interface.
            subinterfaces (list[FixedReferenceNoId]): Child devices to be added to the specified bond interface.
            subnet (ReferenceNoId): Subnet that is associated with the specified network interface.
        """
        if add_subinterfaces is not None:
            self.add_subinterfaces = add_subinterfaces
        if address is not None:
            self.address = address
        if gateway is not None:
            self.gateway = gateway
        if mtu is not None:
            self.mtu = mtu
        if netmask is not None:
            self.netmask = netmask
        if remove_subinterfaces is not None:
            self.remove_subinterfaces = remove_subinterfaces
        if subinterfaces is not None:
            self.subinterfaces = subinterfaces
        if subnet is not None:
            self.subnet = subnet

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `NetworkinterfacepatchEth`".format(key))
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
        if issubclass(NetworkinterfacepatchEth, dict):
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
        if not isinstance(other, NetworkinterfacepatchEth):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
