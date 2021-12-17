# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.11
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_11 import models

class SyslogServerSettings(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'ca_certificate': 'str',
        'tls_audit_enabled': 'bool',
        'logging_severity': 'str'
    }

    attribute_map = {
        'ca_certificate': 'ca_certificate',
        'tls_audit_enabled': 'tls_audit_enabled',
        'logging_severity': 'logging_severity'
    }

    required_args = {
    }

    def __init__(
        self,
        ca_certificate=None,  # type: str
        tls_audit_enabled=None,  # type: bool
        logging_severity=None,  # type: str
    ):
        """
        Keyword args:
            ca_certificate (str): The certificate of the certificate authority (CA) that signed the directory servers' certificate(s), which is used to validate the authenticity of the configured servers.
            tls_audit_enabled (bool): Returns a value of `true` if messages that are necessary in order to audit TLS negotiations performed by the array are forwarded to the configured syslog servers.
            logging_severity (str): Returns the configured logging severity threshold for which events will be forwarded to the configured syslog servers. Default configuration is info level severity. Valid values are `debug`, `info`, and `notice`.
        """
        if ca_certificate is not None:
            self.ca_certificate = ca_certificate
        if tls_audit_enabled is not None:
            self.tls_audit_enabled = tls_audit_enabled
        if logging_severity is not None:
            self.logging_severity = logging_severity

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `SyslogServerSettings`".format(key))
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
        if issubclass(SyslogServerSettings, dict):
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
        if not isinstance(other, SyslogServerSettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
