# coding: utf-8

"""
    Klaviyo API

    Empowering creators to own their destiny  # noqa: E501

    OpenAPI spec version: 2021.11.26
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InlineResponse20012Data(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'email': 'str',
        'status': 'str',
        'customer_id': 'str',
        'variation_id': 'str'
    }

    attribute_map = {
        'email': 'email',
        'status': 'status',
        'customer_id': 'customer_id',
        'variation_id': 'variation_id'
    }

    def __init__(self, email=None, status=None, customer_id=None, variation_id=None):  # noqa: E501
        """InlineResponse20012Data - a model defined in Swagger"""  # noqa: E501
        self._email = None
        self._status = None
        self._customer_id = None
        self._variation_id = None
        self.discriminator = None
        if email is not None:
            self.email = email
        if status is not None:
            self.status = status
        if customer_id is not None:
            self.customer_id = customer_id
        if variation_id is not None:
            self.variation_id = variation_id

    @property
    def email(self):
        """Gets the email of this InlineResponse20012Data.  # noqa: E501


        :return: The email of this InlineResponse20012Data.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this InlineResponse20012Data.


        :param email: The email of this InlineResponse20012Data.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def status(self):
        """Gets the status of this InlineResponse20012Data.  # noqa: E501


        :return: The status of this InlineResponse20012Data.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse20012Data.


        :param status: The status of this InlineResponse20012Data.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def customer_id(self):
        """Gets the customer_id of this InlineResponse20012Data.  # noqa: E501


        :return: The customer_id of this InlineResponse20012Data.  # noqa: E501
        :rtype: str
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this InlineResponse20012Data.


        :param customer_id: The customer_id of this InlineResponse20012Data.  # noqa: E501
        :type: str
        """

        self._customer_id = customer_id

    @property
    def variation_id(self):
        """Gets the variation_id of this InlineResponse20012Data.  # noqa: E501


        :return: The variation_id of this InlineResponse20012Data.  # noqa: E501
        :rtype: str
        """
        return self._variation_id

    @variation_id.setter
    def variation_id(self, variation_id):
        """Sets the variation_id of this InlineResponse20012Data.


        :param variation_id: The variation_id of this InlineResponse20012Data.  # noqa: E501
        :type: str
        """

        self._variation_id = variation_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(InlineResponse20012Data, dict):
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
        if not isinstance(other, InlineResponse20012Data):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
