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

class NetworkInterfacePerformanceEth(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'other_errors_per_sec': 'int',
        'received_bytes_per_sec': 'int',
        'received_crc_errors_per_sec': 'int',
        'received_frame_errors_per_sec': 'int',
        'received_packets_per_sec': 'int',
        'total_errors_per_sec': 'int',
        'transmitted_bytes_per_sec': 'int',
        'transmitted_carrier_errors_per_sec': 'int',
        'transmitted_dropped_errors_per_sec': 'int',
        'transmitted_packets_per_sec': 'int'
    }

    attribute_map = {
        'other_errors_per_sec': 'other_errors_per_sec',
        'received_bytes_per_sec': 'received_bytes_per_sec',
        'received_crc_errors_per_sec': 'received_crc_errors_per_sec',
        'received_frame_errors_per_sec': 'received_frame_errors_per_sec',
        'received_packets_per_sec': 'received_packets_per_sec',
        'total_errors_per_sec': 'total_errors_per_sec',
        'transmitted_bytes_per_sec': 'transmitted_bytes_per_sec',
        'transmitted_carrier_errors_per_sec': 'transmitted_carrier_errors_per_sec',
        'transmitted_dropped_errors_per_sec': 'transmitted_dropped_errors_per_sec',
        'transmitted_packets_per_sec': 'transmitted_packets_per_sec'
    }

    required_args = {
    }

    def __init__(
        self,
        other_errors_per_sec=None,  # type: int
        received_bytes_per_sec=None,  # type: int
        received_crc_errors_per_sec=None,  # type: int
        received_frame_errors_per_sec=None,  # type: int
        received_packets_per_sec=None,  # type: int
        total_errors_per_sec=None,  # type: int
        transmitted_bytes_per_sec=None,  # type: int
        transmitted_carrier_errors_per_sec=None,  # type: int
        transmitted_dropped_errors_per_sec=None,  # type: int
        transmitted_packets_per_sec=None,  # type: int
    ):
        """
        Keyword args:
            other_errors_per_sec (int): The sum of unspecified reception and transmission errors per second.
            received_bytes_per_sec (int): Bytes received per second.
            received_crc_errors_per_sec (int): Reception CRC errors per second.
            received_frame_errors_per_sec (int): Received packet frame errors per second.
            received_packets_per_sec (int): Packets received per second.
            total_errors_per_sec (int): The sum of all reception and transmission errors per second.
            transmitted_bytes_per_sec (int): Bytes transmitted per second.
            transmitted_carrier_errors_per_sec (int): Transmission carrier errors per second.
            transmitted_dropped_errors_per_sec (int): Transmitted packets dropped per second.
            transmitted_packets_per_sec (int): Packets transmitted per second.
        """
        if other_errors_per_sec is not None:
            self.other_errors_per_sec = other_errors_per_sec
        if received_bytes_per_sec is not None:
            self.received_bytes_per_sec = received_bytes_per_sec
        if received_crc_errors_per_sec is not None:
            self.received_crc_errors_per_sec = received_crc_errors_per_sec
        if received_frame_errors_per_sec is not None:
            self.received_frame_errors_per_sec = received_frame_errors_per_sec
        if received_packets_per_sec is not None:
            self.received_packets_per_sec = received_packets_per_sec
        if total_errors_per_sec is not None:
            self.total_errors_per_sec = total_errors_per_sec
        if transmitted_bytes_per_sec is not None:
            self.transmitted_bytes_per_sec = transmitted_bytes_per_sec
        if transmitted_carrier_errors_per_sec is not None:
            self.transmitted_carrier_errors_per_sec = transmitted_carrier_errors_per_sec
        if transmitted_dropped_errors_per_sec is not None:
            self.transmitted_dropped_errors_per_sec = transmitted_dropped_errors_per_sec
        if transmitted_packets_per_sec is not None:
            self.transmitted_packets_per_sec = transmitted_packets_per_sec

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `NetworkInterfacePerformanceEth`".format(key))
        if key == "other_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `other_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_crc_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_crc_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_frame_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_frame_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_packets_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_packets_per_sec`, must be a value greater than or equal to `0`")
        if key == "total_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `total_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "transmitted_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `transmitted_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "transmitted_carrier_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `transmitted_carrier_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "transmitted_dropped_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `transmitted_dropped_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "transmitted_packets_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `transmitted_packets_per_sec`, must be a value greater than or equal to `0`")
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
        if issubclass(NetworkInterfacePerformanceEth, dict):
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
        if not isinstance(other, NetworkInterfacePerformanceEth):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
