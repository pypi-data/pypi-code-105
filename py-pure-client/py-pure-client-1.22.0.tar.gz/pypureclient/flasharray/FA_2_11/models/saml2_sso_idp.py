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

class Saml2SsoIdp(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'entity_id': 'str',
        'url': 'str',
        'metadata_url': 'str',
        'sign_request_enabled': 'bool',
        'encrypt_assertion_enabled': 'bool',
        'verification_certificate': 'str'
    }

    attribute_map = {
        'entity_id': 'entity_id',
        'url': 'url',
        'metadata_url': 'metadata_url',
        'sign_request_enabled': 'sign_request_enabled',
        'encrypt_assertion_enabled': 'encrypt_assertion_enabled',
        'verification_certificate': 'verification_certificate'
    }

    required_args = {
    }

    def __init__(
        self,
        entity_id=None,  # type: str
        url=None,  # type: str
        metadata_url=None,  # type: str
        sign_request_enabled=None,  # type: bool
        encrypt_assertion_enabled=None,  # type: bool
        verification_certificate=None,  # type: str
    ):
        """
        Keyword args:
            entity_id (str): A globally unique name for the identity provider.
            url (str): The URL of the identity provider.
            metadata_url (str): The URL of the identity provider metadata.
            sign_request_enabled (bool): If set to `true`, SAML requests will be signed by the service provider.
            encrypt_assertion_enabled (bool): If set to `true`, SAML assertions will be encrypted by the identity provider.
            verification_certificate (str): The X509 certificate that the service provider uses to verify the SAML response signature from the identity provider.
        """
        if entity_id is not None:
            self.entity_id = entity_id
        if url is not None:
            self.url = url
        if metadata_url is not None:
            self.metadata_url = metadata_url
        if sign_request_enabled is not None:
            self.sign_request_enabled = sign_request_enabled
        if encrypt_assertion_enabled is not None:
            self.encrypt_assertion_enabled = encrypt_assertion_enabled
        if verification_certificate is not None:
            self.verification_certificate = verification_certificate

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Saml2SsoIdp`".format(key))
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
        if issubclass(Saml2SsoIdp, dict):
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
        if not isinstance(other, Saml2SsoIdp):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
