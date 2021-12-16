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

class TrackPayloadProperties(object):
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
        'event_id': 'str',
        'value': 'str',
        'your_custom_field': 'OneOftrackPayloadPropertiesYourCustomField'
    }

    attribute_map = {
        'event_id': '$event_id',
        'value': '$value',
        'your_custom_field': 'YOUR_CUSTOM_FIELD'
    }

    def __init__(self, event_id=None, value=None, your_custom_field=None):  # noqa: E501
        """TrackPayloadProperties - a model defined in Swagger"""  # noqa: E501
        self._event_id = None
        self._value = None
        self._your_custom_field = None
        self.discriminator = None
        if event_id is not None:
            self.event_id = event_id
        if value is not None:
            self.value = value
        if your_custom_field is not None:
            self.your_custom_field = your_custom_field

    @property
    def event_id(self):
        """Gets the event_id of this TrackPayloadProperties.  # noqa: E501


        :return: The event_id of this TrackPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        """Sets the event_id of this TrackPayloadProperties.


        :param event_id: The event_id of this TrackPayloadProperties.  # noqa: E501
        :type: str
        """

        self._event_id = event_id

    @property
    def value(self):
        """Gets the value of this TrackPayloadProperties.  # noqa: E501


        :return: The value of this TrackPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this TrackPayloadProperties.


        :param value: The value of this TrackPayloadProperties.  # noqa: E501
        :type: str
        """

        self._value = value

    @property
    def your_custom_field(self):
        """Gets the your_custom_field of this TrackPayloadProperties.  # noqa: E501


        :return: The your_custom_field of this TrackPayloadProperties.  # noqa: E501
        :rtype: OneOftrackPayloadPropertiesYourCustomField
        """
        return self._your_custom_field

    @your_custom_field.setter
    def your_custom_field(self, your_custom_field):
        """Sets the your_custom_field of this TrackPayloadProperties.


        :param your_custom_field: The your_custom_field of this TrackPayloadProperties.  # noqa: E501
        :type: OneOftrackPayloadPropertiesYourCustomField
        """

        self._your_custom_field = your_custom_field

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
        if issubclass(TrackPayloadProperties, dict):
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
        if not isinstance(other, TrackPayloadProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
