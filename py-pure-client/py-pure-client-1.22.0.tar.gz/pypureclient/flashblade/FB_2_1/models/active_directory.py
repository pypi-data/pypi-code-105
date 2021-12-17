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

class ActiveDirectory(object):
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
        'computer_name': 'str',
        'directory_servers': 'list[str]',
        'domain': 'str',
        'encryption_types': 'list[str]',
        'join_ou': 'str',
        'kerberos_servers': 'list[str]',
        'service_principal_names': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'computer_name': 'computer_name',
        'directory_servers': 'directory_servers',
        'domain': 'domain',
        'encryption_types': 'encryption_types',
        'join_ou': 'join_ou',
        'kerberos_servers': 'kerberos_servers',
        'service_principal_names': 'service_principal_names'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        id=None,  # type: str
        computer_name=None,  # type: str
        directory_servers=None,  # type: List[str]
        domain=None,  # type: str
        encryption_types=None,  # type: List[str]
        join_ou=None,  # type: str
        kerberos_servers=None,  # type: List[str]
        service_principal_names=None,  # type: List[str]
    ):
        """
        Keyword args:
            name (str): Name of the object (e.g., a file system or snapshot).
            id (str): A non-modifiable, globally unique ID chosen by the system.
            computer_name (str): The common name of the computer account to be created in the Active Directory domain. If not specified, defaults to the name of the Active Directory configuration.
            directory_servers (list[str]): A list of directory servers that will be used for lookups related to user authorization. Accepted server formats are IP address and DNS name. All specified servers must be registered to the domain appropriately in the array's configured DNS and will only be communicated with over the secure LDAP (LDAPS) protocol.
            domain (str): The Active Directory domain to join.
            encryption_types (list[str]): The encryption types that are supported for use by clients for Kerberos authentication.
            join_ou (str): The relative distinguished name of the organizational unit in which the computer account was created when joining the domain.
            kerberos_servers (list[str]): A list of key distribution servers to use for Kerberos protocol. Accepted server formats are IP address and DNS name. All specified servers must be registered to the domain appropriately in the array's configured DNS.
            service_principal_names (list[str]): A list of service principal names registered for the machine account, which can be used for the creation of keys for Kerberos authentication.
        """
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if computer_name is not None:
            self.computer_name = computer_name
        if directory_servers is not None:
            self.directory_servers = directory_servers
        if domain is not None:
            self.domain = domain
        if encryption_types is not None:
            self.encryption_types = encryption_types
        if join_ou is not None:
            self.join_ou = join_ou
        if kerberos_servers is not None:
            self.kerberos_servers = kerberos_servers
        if service_principal_names is not None:
            self.service_principal_names = service_principal_names

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `ActiveDirectory`".format(key))
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
        if issubclass(ActiveDirectory, dict):
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
        if not isinstance(other, ActiveDirectory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
