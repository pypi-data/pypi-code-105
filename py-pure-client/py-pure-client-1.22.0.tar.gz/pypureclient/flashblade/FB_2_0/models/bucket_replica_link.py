# coding: utf-8

"""
    FlashBlade REST API Client

    A lightweight client for FlashBlade REST API 2.0, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flashblade.FB_2_0 import models

class BucketReplicaLink(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'direction': 'Direction',
        'lag': 'int',
        'status_details': 'str',
        'local_bucket': 'FixedReference',
        'paused': 'bool',
        'recovery_point': 'int',
        'remote': 'FixedReference',
        'remote_bucket': 'FixedReferenceNameOnly',
        'remote_credentials': 'Reference',
        'status': 'str'
    }

    attribute_map = {
        'id': 'id',
        'direction': 'direction',
        'lag': 'lag',
        'status_details': 'status_details',
        'local_bucket': 'local_bucket',
        'paused': 'paused',
        'recovery_point': 'recovery_point',
        'remote': 'remote',
        'remote_bucket': 'remote_bucket',
        'remote_credentials': 'remote_credentials',
        'status': 'status'
    }

    required_args = {
    }

    def __init__(
        self,
        id=None,  # type: str
        direction=None,  # type: models.Direction
        lag=None,  # type: int
        status_details=None,  # type: str
        local_bucket=None,  # type: models.FixedReference
        paused=None,  # type: bool
        recovery_point=None,  # type: int
        remote=None,  # type: models.FixedReference
        remote_bucket=None,  # type: models.FixedReferenceNameOnly
        remote_credentials=None,  # type: models.Reference
        status=None,  # type: str
    ):
        """
        Keyword args:
            id (str): A non-modifiable, globally unique ID chosen by the system.
            direction (Direction)
            lag (int): Duration in milliseconds that represents how far behind the replication target is from the source. This is the time difference between current time and `recovery_point`.
            status_details (str): Detailed information about the status of the replica link when it is unhealthy.
            local_bucket (FixedReference): Reference to a local bucket.
            paused (bool): Is the replica link paused?
            recovery_point (int): Time, in milliseconds since UNIX epoch, where all object changes before this time are guaranteed to have been replicated. Changes after this time may have been replicated.
            remote (FixedReference): Reference to the associated remote, which can either be a `target` or remote `array`. If it is an `array`, then the `resource-type` field will not be populated.
            remote_bucket (FixedReferenceNameOnly): Reference to a remote bucket.
            remote_credentials (Reference): Reference to a remote-credentials object to access the remote bucket.
            status (str): Status of the replica link. Values include `replicating`, `paused`, and `unhealthy`.
        """
        if id is not None:
            self.id = id
        if direction is not None:
            self.direction = direction
        if lag is not None:
            self.lag = lag
        if status_details is not None:
            self.status_details = status_details
        if local_bucket is not None:
            self.local_bucket = local_bucket
        if paused is not None:
            self.paused = paused
        if recovery_point is not None:
            self.recovery_point = recovery_point
        if remote is not None:
            self.remote = remote
        if remote_bucket is not None:
            self.remote_bucket = remote_bucket
        if remote_credentials is not None:
            self.remote_credentials = remote_credentials
        if status is not None:
            self.status = status

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `BucketReplicaLink`".format(key))
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
        if issubclass(BucketReplicaLink, dict):
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
        if not isinstance(other, BucketReplicaLink):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
