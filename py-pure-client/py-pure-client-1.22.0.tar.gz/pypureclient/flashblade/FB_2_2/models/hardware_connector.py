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

class HardwareConnector(object):
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
        'connector_type': 'str',
        'lane_speed': 'int',
        'port_count': 'int',
        'transceiver_type': 'str'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'connector_type': 'connector_type',
        'lane_speed': 'lane_speed',
        'port_count': 'port_count',
        'transceiver_type': 'transceiver_type'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        id=None,  # type: str
        connector_type=None,  # type: str
        lane_speed=None,  # type: int
        port_count=None,  # type: int
        transceiver_type=None,  # type: str
    ):
        """
        Keyword args:
            name (str): Name of the object (e.g., a file system or snapshot).
            id (str): A non-modifiable, globally unique ID chosen by the system.
            connector_type (str): Form-factor of the interface. Valid values include `QSFP` and `RJ-45`.
            lane_speed (int): Configured speed of each lane in the connector in bits-per-second.
            port_count (int): Configured number of ports in the connector (1/4 for QSFP).
            transceiver_type (str): Details about the transceiver which is plugged into the connector port. Transceiver type will be read-only for pureuser. If nothing is plugged into QSFP port, value will be `Unused` and type cannot be auto-detected, and internal user has not specified a type - value will be `Unknown`. If transceiver is plugged in, and type is auto-detected, and/or type has been explicitly set by internal user - that value will be shown. Transceiver type is not applicable for RJ-45 connectors.
        """
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if connector_type is not None:
            self.connector_type = connector_type
        if lane_speed is not None:
            self.lane_speed = lane_speed
        if port_count is not None:
            self.port_count = port_count
        if transceiver_type is not None:
            self.transceiver_type = transceiver_type

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `HardwareConnector`".format(key))
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
        if issubclass(HardwareConnector, dict):
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
        if not isinstance(other, HardwareConnector):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
