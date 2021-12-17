# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.10
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_10 import models

class OffloadS3(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'access_key_id': 'str',
        'bucket': 'str',
        'placement_strategy': 'str',
        'secret_access_key': 'str',
        'uri': 'str'
    }

    attribute_map = {
        'access_key_id': 'access_key_id',
        'bucket': 'bucket',
        'placement_strategy': 'placement_strategy',
        'secret_access_key': 'secret_access_key',
        'uri': 'uri'
    }

    required_args = {
    }

    def __init__(
        self,
        access_key_id=None,  # type: str
        bucket=None,  # type: str
        placement_strategy=None,  # type: str
        secret_access_key=None,  # type: str
        uri=None,  # type: str
    ):
        """
        Keyword args:
            access_key_id (str): The access key ID of the AWS account used to create a connection between the array and an Amazon S3 offload target. The access key ID is 20 characters in length and is only accepted when creating the connection between the array and the S3 offload target. The `access_key_id`, `secret_access_key`, and `bucket` parameters must be set together.
            bucket (str): The name of the Amazon S3 bucket to where the data will be offloaded. Grant basic read and write ACL permissions to the bucket, and enable default (server-side) encryption for the bucket. Also verify that the bucket is empty of all objects and does not have any lifecycle policies. The `access_key_id`, `secret_access_key`, and `bucket` parameters must be set together.
            placement_strategy (str): The storage placement strategy used for the dynamic placement of data in an Amazon S3 offload target. Valid values are `aws-intelligent-tiering`, `aws-standard-class`, and `retention-based`. If set to `aws-intelligent-tiering`, data is stored in the Amazon S3 INTELLIGENT_TIERING storage class regardless of the retention period. If set to `aws-standard-access`, the data is stored in the Amazon S3 STANDARD storage class regardless of the retention period. If set to `retention-based`, the data for protection groups with longer retention periods is placed in the Amazon S3 STANDARD_IA (infrequently accessed, more cost-effective) storage class. All other data is placed in the STANDARD storage class. When the array is initially connected to an S3 offload target, `placement_strategy` is automatically set to `retention-based`. The `placement_strategy` and `uri` parameters cannot be set together.
            secret_access_key (str): The secret access key that goes with the access key ID (`access_key_id`) of the AWS account. The secret access key is 40 characters in length is only accepted when creating the connection between the array and the S3 offload target. The `access_key_id`, `secret_access_key`, and `bucket` parameters must be set together.
            uri (str): The URI used to create a connection between the array and a non-AWS S3 offload target. Storage placement strategies are not supported for non-AWS S3 offload targets. Both the HTTP and HTTPS protocols are allowed.
        """
        if access_key_id is not None:
            self.access_key_id = access_key_id
        if bucket is not None:
            self.bucket = bucket
        if placement_strategy is not None:
            self.placement_strategy = placement_strategy
        if secret_access_key is not None:
            self.secret_access_key = secret_access_key
        if uri is not None:
            self.uri = uri

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `OffloadS3`".format(key))
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
        if issubclass(OffloadS3, dict):
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
        if not isinstance(other, OffloadS3):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
