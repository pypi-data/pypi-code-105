# coding: utf-8

"""
    FlashBlade REST API

    A lightweight client for FlashBlade REST API 2.1, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flashblade.FB_2_1 import models

class MultiProtocolPost(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'access_control_style': 'str',
        'safeguard_acls': 'bool'
    }

    attribute_map = {
        'access_control_style': 'access_control_style',
        'safeguard_acls': 'safeguard_acls'
    }

    required_args = {
    }

    def __init__(
        self,
        access_control_style=None,  # type: str
        safeguard_acls=None,  # type: bool
    ):
        """
        Keyword args:
            access_control_style (str): The access control style that is utilized for client actions such as setting file and directory ACLs. Possible values include `nfs`, `smb`, `shared`, `independent`, and `mode-bits`. If `nfs` is specified, then SMB clients will be unable to set permissions on files and directories. If `smb` is specified, then NFS clients will be unable to set permissions on files and directories. If `shared` is specified, then NFS and SMB clients will both be able to set permissions on files and directories. Any client will be able to overwrite the permissions set by another client, regardless of protocol. If `independent` is specified, then NFS and SMB clients will both be able to set permissions on files and directories, and can access files and directories created over any protocol. Permissions set by SMB clients will not affect NFS clients and vice versa. NFS clients will be restricted to only using mode bits to set permissions. If `mode-bits` is specified, then NFS and SMB clients will both be able to set permissions on files and directories, but only mode bits may be used to set permissions for NFS clients. When SMB clients set an ACL, it will be converted to have the same permission granularity as NFS mode bits. Defaults to `shared`.
            safeguard_acls (bool): If set to `true`, prevents NFS clients from erasing a configured ACL when setting NFS mode bits. If this is `true`, then attempts to set mode bits on a file or directory will fail if they cannot be combined with the existing ACL set on a file or directory without erasing the ACL. Attempts to set mode bits that would not erase an existing ACL will still succeed and the mode bit changes will be merged with the existing ACL. This must be `false` when `access_control_style` is set to either `independent` or `mode-bits`. Defaults to `true`.
        """
        if access_control_style is not None:
            self.access_control_style = access_control_style
        if safeguard_acls is not None:
            self.safeguard_acls = safeguard_acls

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `MultiProtocolPost`".format(key))
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
        if issubclass(MultiProtocolPost, dict):
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
        if not isinstance(other, MultiProtocolPost):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
