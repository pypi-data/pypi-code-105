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

class TemplateIdSendBody(object):
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
        'from_email': 'str',
        'from_name': 'str',
        'subject': 'str',
        'to': 'str',
        'context': 'str'
    }

    attribute_map = {
        'from_email': 'from_email',
        'from_name': 'from_name',
        'subject': 'subject',
        'to': 'to',
        'context': 'context'
    }

    def __init__(self, from_email='george.washington@klaviyo.com', from_name='George Washington', subject='Happy Fourth!', to='[{"name":"Abraham Lincoln","email":"abraham.lincoln@klaviyo.com"}]', context='{ "name" : "George Washington", "state" : "VA" }'):  # noqa: E501
        """TemplateIdSendBody - a model defined in Swagger"""  # noqa: E501
        self._from_email = None
        self._from_name = None
        self._subject = None
        self._to = None
        self._context = None
        self.discriminator = None
        self.from_email = from_email
        self.from_name = from_name
        self.subject = subject
        self.to = to
        if context is not None:
            self.context = context

    @property
    def from_email(self):
        """Gets the from_email of this TemplateIdSendBody.  # noqa: E501


        :return: The from_email of this TemplateIdSendBody.  # noqa: E501
        :rtype: str
        """
        return self._from_email

    @from_email.setter
    def from_email(self, from_email):
        """Sets the from_email of this TemplateIdSendBody.


        :param from_email: The from_email of this TemplateIdSendBody.  # noqa: E501
        :type: str
        """
        if from_email is None:
            raise ValueError("Invalid value for `from_email`, must not be `None`")  # noqa: E501

        self._from_email = from_email

    @property
    def from_name(self):
        """Gets the from_name of this TemplateIdSendBody.  # noqa: E501


        :return: The from_name of this TemplateIdSendBody.  # noqa: E501
        :rtype: str
        """
        return self._from_name

    @from_name.setter
    def from_name(self, from_name):
        """Sets the from_name of this TemplateIdSendBody.


        :param from_name: The from_name of this TemplateIdSendBody.  # noqa: E501
        :type: str
        """
        if from_name is None:
            raise ValueError("Invalid value for `from_name`, must not be `None`")  # noqa: E501

        self._from_name = from_name

    @property
    def subject(self):
        """Gets the subject of this TemplateIdSendBody.  # noqa: E501


        :return: The subject of this TemplateIdSendBody.  # noqa: E501
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this TemplateIdSendBody.


        :param subject: The subject of this TemplateIdSendBody.  # noqa: E501
        :type: str
        """
        if subject is None:
            raise ValueError("Invalid value for `subject`, must not be `None`")  # noqa: E501

        self._subject = subject

    @property
    def to(self):
        """Gets the to of this TemplateIdSendBody.  # noqa: E501

        **Mixed**. string, or JSON encoded array of objects with \"email\" and \"name\" keys. `abraham.lincoln@klaviyo.com` OR `[{\"name\":\"Abraham Lincoln\",\"email\":\"abraham.lincoln@klaviyo.com\"}]`   # noqa: E501

        :return: The to of this TemplateIdSendBody.  # noqa: E501
        :rtype: str
        """
        return self._to

    @to.setter
    def to(self, to):
        """Sets the to of this TemplateIdSendBody.

        **Mixed**. string, or JSON encoded array of objects with \"email\" and \"name\" keys. `abraham.lincoln@klaviyo.com` OR `[{\"name\":\"Abraham Lincoln\",\"email\":\"abraham.lincoln@klaviyo.com\"}]`   # noqa: E501

        :param to: The to of this TemplateIdSendBody.  # noqa: E501
        :type: str
        """
        if to is None:
            raise ValueError("Invalid value for `to`, must not be `None`")  # noqa: E501

        self._to = to

    @property
    def context(self):
        """Gets the context of this TemplateIdSendBody.  # noqa: E501

        Optional, JSON object. This is the context your email template will be rendered with. Email templates are rendered with contexts in a similar manner to how Django templates are rendered. This means that nested template variables can be referenced via dot notation and template variables without corresponding context values are treated as falsy and output nothing. ex: `{ \"name\" : \"George Washington\", \"state\" : \"VA\" }`   # noqa: E501

        :return: The context of this TemplateIdSendBody.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this TemplateIdSendBody.

        Optional, JSON object. This is the context your email template will be rendered with. Email templates are rendered with contexts in a similar manner to how Django templates are rendered. This means that nested template variables can be referenced via dot notation and template variables without corresponding context values are treated as falsy and output nothing. ex: `{ \"name\" : \"George Washington\", \"state\" : \"VA\" }`   # noqa: E501

        :param context: The context of this TemplateIdSendBody.  # noqa: E501
        :type: str
        """

        self._context = context

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
        if issubclass(TemplateIdSendBody, dict):
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
        if not isinstance(other, TemplateIdSendBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
