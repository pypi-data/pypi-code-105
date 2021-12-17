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

class ResourcePerformanceByArray(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'bytes_per_mirrored_write': 'int',
        'bytes_per_op': 'int',
        'bytes_per_read': 'int',
        'bytes_per_write': 'int',
        'mirrored_write_bytes_per_sec': 'int',
        'mirrored_writes_per_sec': 'int',
        'qos_rate_limit_usec_per_mirrored_write_op': 'int',
        'qos_rate_limit_usec_per_read_op': 'int',
        'qos_rate_limit_usec_per_write_op': 'int',
        'queue_usec_per_mirrored_write_op': 'int',
        'queue_usec_per_read_op': 'int',
        'queue_usec_per_write_op': 'int',
        'read_bytes_per_sec': 'int',
        'reads_per_sec': 'int',
        'san_usec_per_mirrored_write_op': 'int',
        'san_usec_per_read_op': 'int',
        'san_usec_per_write_op': 'int',
        'service_usec_per_mirrored_write_op': 'int',
        'service_usec_per_read_op': 'int',
        'service_usec_per_write_op': 'int',
        'time': 'int',
        'usec_per_mirrored_write_op': 'int',
        'usec_per_read_op': 'int',
        'usec_per_write_op': 'int',
        'write_bytes_per_sec': 'int',
        'writes_per_sec': 'int',
        'service_usec_per_read_op_cache_reduction': 'float',
        'id': 'str',
        'name': 'str',
        'array': 'Resource'
    }

    attribute_map = {
        'bytes_per_mirrored_write': 'bytes_per_mirrored_write',
        'bytes_per_op': 'bytes_per_op',
        'bytes_per_read': 'bytes_per_read',
        'bytes_per_write': 'bytes_per_write',
        'mirrored_write_bytes_per_sec': 'mirrored_write_bytes_per_sec',
        'mirrored_writes_per_sec': 'mirrored_writes_per_sec',
        'qos_rate_limit_usec_per_mirrored_write_op': 'qos_rate_limit_usec_per_mirrored_write_op',
        'qos_rate_limit_usec_per_read_op': 'qos_rate_limit_usec_per_read_op',
        'qos_rate_limit_usec_per_write_op': 'qos_rate_limit_usec_per_write_op',
        'queue_usec_per_mirrored_write_op': 'queue_usec_per_mirrored_write_op',
        'queue_usec_per_read_op': 'queue_usec_per_read_op',
        'queue_usec_per_write_op': 'queue_usec_per_write_op',
        'read_bytes_per_sec': 'read_bytes_per_sec',
        'reads_per_sec': 'reads_per_sec',
        'san_usec_per_mirrored_write_op': 'san_usec_per_mirrored_write_op',
        'san_usec_per_read_op': 'san_usec_per_read_op',
        'san_usec_per_write_op': 'san_usec_per_write_op',
        'service_usec_per_mirrored_write_op': 'service_usec_per_mirrored_write_op',
        'service_usec_per_read_op': 'service_usec_per_read_op',
        'service_usec_per_write_op': 'service_usec_per_write_op',
        'time': 'time',
        'usec_per_mirrored_write_op': 'usec_per_mirrored_write_op',
        'usec_per_read_op': 'usec_per_read_op',
        'usec_per_write_op': 'usec_per_write_op',
        'write_bytes_per_sec': 'write_bytes_per_sec',
        'writes_per_sec': 'writes_per_sec',
        'service_usec_per_read_op_cache_reduction': 'service_usec_per_read_op_cache_reduction',
        'id': 'id',
        'name': 'name',
        'array': 'array'
    }

    required_args = {
    }

    def __init__(
        self,
        bytes_per_mirrored_write=None,  # type: int
        bytes_per_op=None,  # type: int
        bytes_per_read=None,  # type: int
        bytes_per_write=None,  # type: int
        mirrored_write_bytes_per_sec=None,  # type: int
        mirrored_writes_per_sec=None,  # type: int
        qos_rate_limit_usec_per_mirrored_write_op=None,  # type: int
        qos_rate_limit_usec_per_read_op=None,  # type: int
        qos_rate_limit_usec_per_write_op=None,  # type: int
        queue_usec_per_mirrored_write_op=None,  # type: int
        queue_usec_per_read_op=None,  # type: int
        queue_usec_per_write_op=None,  # type: int
        read_bytes_per_sec=None,  # type: int
        reads_per_sec=None,  # type: int
        san_usec_per_mirrored_write_op=None,  # type: int
        san_usec_per_read_op=None,  # type: int
        san_usec_per_write_op=None,  # type: int
        service_usec_per_mirrored_write_op=None,  # type: int
        service_usec_per_read_op=None,  # type: int
        service_usec_per_write_op=None,  # type: int
        time=None,  # type: int
        usec_per_mirrored_write_op=None,  # type: int
        usec_per_read_op=None,  # type: int
        usec_per_write_op=None,  # type: int
        write_bytes_per_sec=None,  # type: int
        writes_per_sec=None,  # type: int
        service_usec_per_read_op_cache_reduction=None,  # type: float
        id=None,  # type: str
        name=None,  # type: str
        array=None,  # type: models.Resource
    ):
        """
        Keyword args:
            bytes_per_mirrored_write (int): The average I/O size per mirrored write. Measured in bytes.
            bytes_per_op (int): The average I/O size for both read and write (all) operations.
            bytes_per_read (int): The average I/O size per read. Measured in bytes.
            bytes_per_write (int): The average I/O size per write. Measured in bytes.
            mirrored_write_bytes_per_sec (int): The number of mirrored bytes written per second.
            mirrored_writes_per_sec (int): The number of mirrored writes per second.
            qos_rate_limit_usec_per_mirrored_write_op (int): The average time it takes the array to process a mirrored I/O write request. Measured in microseconds.
            qos_rate_limit_usec_per_read_op (int): The average time spent waiting due to QoS rate limiting for a read request. Measured in microseconds.
            qos_rate_limit_usec_per_write_op (int): The average time that a write I/O request spends waiting as a result of the volume reaching its QoS bandwidth limit. Measured in microseconds.
            queue_usec_per_mirrored_write_op (int): The average time that a mirrored write I/O request spends in the array waiting to be served. Measured in microseconds.
            queue_usec_per_read_op (int): The average time that a read I/O request spends in the array waiting to be served. Measured in microseconds.
            queue_usec_per_write_op (int): The average time that a write I/O request spends in the array waiting to be served. Measured in microseconds.
            read_bytes_per_sec (int): The number of bytes read per second.
            reads_per_sec (int): The number of read requests processed per second.
            san_usec_per_mirrored_write_op (int): The average time required to transfer data from the initiator to the array for a mirrored write request. Measured in microseconds.
            san_usec_per_read_op (int): The average time required to transfer data from the array to the initiator for a read request. Measured in microseconds.
            san_usec_per_write_op (int): The average time required to transfer data from the initiator to the array for a write request. Measured in microseconds.
            service_usec_per_mirrored_write_op (int): The average time required for the array to service a mirrored write request. Measured in microseconds.
            service_usec_per_read_op (int): The average time required for the array to service a read request. Measured in microseconds.
            service_usec_per_write_op (int): The average time required for the array to service a write request. Measured in microseconds.
            time (int): The time when the sample performance data was taken. Measured in milliseconds since the UNIX epoch.
            usec_per_mirrored_write_op (int): The average time it takes the array to process a mirrored I/O write request. Measured in microseconds. The average time does not include SAN time, queue time, or QoS rate limit time.
            usec_per_read_op (int): The average time it takes the array to process an I/O read request. Measured in microseconds. The average time does not include SAN time, queue time, or QoS rate limit time.
            usec_per_write_op (int): The average time it takes the array to process an I/O write request. Measured in microseconds. The average time does not include SAN time, queue time, or QoS rate limit time.
            write_bytes_per_sec (int): The number of bytes written per second.
            writes_per_sec (int): The number of write requests processed per second.
            service_usec_per_read_op_cache_reduction (float): The percentage reduction in `service_usec_per_read_op` due to data cache hits. For example, a value of 0.25 indicates that the value of `service_usec_per_read_op` is 25&#37; lower than it would have been without any data cache hits.
            id (str): A globally unique, system-generated ID. The ID cannot be modified and cannot refer to another resource.
            name (str): A user-specified name. The name must be locally unique and can be changed.
            array (Resource): The array on which the performance metrics were recorded.
        """
        if bytes_per_mirrored_write is not None:
            self.bytes_per_mirrored_write = bytes_per_mirrored_write
        if bytes_per_op is not None:
            self.bytes_per_op = bytes_per_op
        if bytes_per_read is not None:
            self.bytes_per_read = bytes_per_read
        if bytes_per_write is not None:
            self.bytes_per_write = bytes_per_write
        if mirrored_write_bytes_per_sec is not None:
            self.mirrored_write_bytes_per_sec = mirrored_write_bytes_per_sec
        if mirrored_writes_per_sec is not None:
            self.mirrored_writes_per_sec = mirrored_writes_per_sec
        if qos_rate_limit_usec_per_mirrored_write_op is not None:
            self.qos_rate_limit_usec_per_mirrored_write_op = qos_rate_limit_usec_per_mirrored_write_op
        if qos_rate_limit_usec_per_read_op is not None:
            self.qos_rate_limit_usec_per_read_op = qos_rate_limit_usec_per_read_op
        if qos_rate_limit_usec_per_write_op is not None:
            self.qos_rate_limit_usec_per_write_op = qos_rate_limit_usec_per_write_op
        if queue_usec_per_mirrored_write_op is not None:
            self.queue_usec_per_mirrored_write_op = queue_usec_per_mirrored_write_op
        if queue_usec_per_read_op is not None:
            self.queue_usec_per_read_op = queue_usec_per_read_op
        if queue_usec_per_write_op is not None:
            self.queue_usec_per_write_op = queue_usec_per_write_op
        if read_bytes_per_sec is not None:
            self.read_bytes_per_sec = read_bytes_per_sec
        if reads_per_sec is not None:
            self.reads_per_sec = reads_per_sec
        if san_usec_per_mirrored_write_op is not None:
            self.san_usec_per_mirrored_write_op = san_usec_per_mirrored_write_op
        if san_usec_per_read_op is not None:
            self.san_usec_per_read_op = san_usec_per_read_op
        if san_usec_per_write_op is not None:
            self.san_usec_per_write_op = san_usec_per_write_op
        if service_usec_per_mirrored_write_op is not None:
            self.service_usec_per_mirrored_write_op = service_usec_per_mirrored_write_op
        if service_usec_per_read_op is not None:
            self.service_usec_per_read_op = service_usec_per_read_op
        if service_usec_per_write_op is not None:
            self.service_usec_per_write_op = service_usec_per_write_op
        if time is not None:
            self.time = time
        if usec_per_mirrored_write_op is not None:
            self.usec_per_mirrored_write_op = usec_per_mirrored_write_op
        if usec_per_read_op is not None:
            self.usec_per_read_op = usec_per_read_op
        if usec_per_write_op is not None:
            self.usec_per_write_op = usec_per_write_op
        if write_bytes_per_sec is not None:
            self.write_bytes_per_sec = write_bytes_per_sec
        if writes_per_sec is not None:
            self.writes_per_sec = writes_per_sec
        if service_usec_per_read_op_cache_reduction is not None:
            self.service_usec_per_read_op_cache_reduction = service_usec_per_read_op_cache_reduction
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if array is not None:
            self.array = array

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `ResourcePerformanceByArray`".format(key))
        if key == "bytes_per_mirrored_write" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_mirrored_write`, must be a value greater than or equal to `0`")
        if key == "bytes_per_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_op`, must be a value greater than or equal to `0`")
        if key == "bytes_per_read" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_read`, must be a value greater than or equal to `0`")
        if key == "bytes_per_write" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_write`, must be a value greater than or equal to `0`")
        if key == "mirrored_write_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `mirrored_write_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "mirrored_writes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `mirrored_writes_per_sec`, must be a value greater than or equal to `0`")
        if key == "qos_rate_limit_usec_per_mirrored_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `qos_rate_limit_usec_per_mirrored_write_op`, must be a value greater than or equal to `0`")
        if key == "qos_rate_limit_usec_per_read_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `qos_rate_limit_usec_per_read_op`, must be a value greater than or equal to `0`")
        if key == "qos_rate_limit_usec_per_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `qos_rate_limit_usec_per_write_op`, must be a value greater than or equal to `0`")
        if key == "queue_usec_per_mirrored_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `queue_usec_per_mirrored_write_op`, must be a value greater than or equal to `0`")
        if key == "queue_usec_per_read_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `queue_usec_per_read_op`, must be a value greater than or equal to `0`")
        if key == "queue_usec_per_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `queue_usec_per_write_op`, must be a value greater than or equal to `0`")
        if key == "read_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `read_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "reads_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `reads_per_sec`, must be a value greater than or equal to `0`")
        if key == "san_usec_per_mirrored_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `san_usec_per_mirrored_write_op`, must be a value greater than or equal to `0`")
        if key == "san_usec_per_read_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `san_usec_per_read_op`, must be a value greater than or equal to `0`")
        if key == "san_usec_per_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `san_usec_per_write_op`, must be a value greater than or equal to `0`")
        if key == "service_usec_per_mirrored_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `service_usec_per_mirrored_write_op`, must be a value greater than or equal to `0`")
        if key == "service_usec_per_read_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `service_usec_per_read_op`, must be a value greater than or equal to `0`")
        if key == "service_usec_per_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `service_usec_per_write_op`, must be a value greater than or equal to `0`")
        if key == "usec_per_mirrored_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `usec_per_mirrored_write_op`, must be a value greater than or equal to `0`")
        if key == "usec_per_read_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `usec_per_read_op`, must be a value greater than or equal to `0`")
        if key == "usec_per_write_op" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `usec_per_write_op`, must be a value greater than or equal to `0`")
        if key == "write_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `write_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "writes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `writes_per_sec`, must be a value greater than or equal to `0`")
        if key == "service_usec_per_read_op_cache_reduction" and value is not None:
            if value > 1.0:
                raise ValueError("Invalid value for `service_usec_per_read_op_cache_reduction`, value must be less than or equal to `1.0`")
            if value < 0.0:
                raise ValueError("Invalid value for `service_usec_per_read_op_cache_reduction`, must be a value greater than or equal to `0.0`")
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
        if issubclass(ResourcePerformanceByArray, dict):
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
        if not isinstance(other, ResourcePerformanceByArray):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
