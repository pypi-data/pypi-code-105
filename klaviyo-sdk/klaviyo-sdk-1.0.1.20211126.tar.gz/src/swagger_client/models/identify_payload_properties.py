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

class IdentifyPayloadProperties(object):
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
        'first_name': 'str',
        'last_name': 'str',
        'phone_number': 'str',
        'title': 'str',
        'organization': 'str',
        'city': 'str',
        'region': 'str',
        'country': 'str',
        'zip': 'str',
        'image': 'str',
        'consent': 'str',
        'your_custom_field': 'OneOfidentifyPayloadPropertiesYourCustomField'
    }

    attribute_map = {
        'email': '$email',
        'first_name': '$first_name',
        'last_name': '$last_name',
        'phone_number': '$phone_number',
        'title': '$title',
        'organization': '$organization',
        'city': '$city',
        'region': '$region',
        'country': '$country',
        'zip': '$zip',
        'image': '$image',
        'consent': '$consent',
        'your_custom_field': 'YOUR_CUSTOM_FIELD'
    }

    def __init__(self, email=None, first_name=None, last_name=None, phone_number=None, title=None, organization=None, city=None, region=None, country=None, zip=None, image=None, consent=None, your_custom_field=None):  # noqa: E501
        """IdentifyPayloadProperties - a model defined in Swagger"""  # noqa: E501
        self._email = None
        self._first_name = None
        self._last_name = None
        self._phone_number = None
        self._title = None
        self._organization = None
        self._city = None
        self._region = None
        self._country = None
        self._zip = None
        self._image = None
        self._consent = None
        self._your_custom_field = None
        self.discriminator = None
        if email is not None:
            self.email = email
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if phone_number is not None:
            self.phone_number = phone_number
        if title is not None:
            self.title = title
        if organization is not None:
            self.organization = organization
        if city is not None:
            self.city = city
        if region is not None:
            self.region = region
        if country is not None:
            self.country = country
        if zip is not None:
            self.zip = zip
        if image is not None:
            self.image = image
        if consent is not None:
            self.consent = consent
        if your_custom_field is not None:
            self.your_custom_field = your_custom_field

    @property
    def email(self):
        """Gets the email of this IdentifyPayloadProperties.  # noqa: E501


        :return: The email of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this IdentifyPayloadProperties.


        :param email: The email of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def first_name(self):
        """Gets the first_name of this IdentifyPayloadProperties.  # noqa: E501


        :return: The first_name of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this IdentifyPayloadProperties.


        :param first_name: The first_name of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this IdentifyPayloadProperties.  # noqa: E501


        :return: The last_name of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this IdentifyPayloadProperties.


        :param last_name: The last_name of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._last_name = last_name

    @property
    def phone_number(self):
        """Gets the phone_number of this IdentifyPayloadProperties.  # noqa: E501


        :return: The phone_number of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """Sets the phone_number of this IdentifyPayloadProperties.


        :param phone_number: The phone_number of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._phone_number = phone_number

    @property
    def title(self):
        """Gets the title of this IdentifyPayloadProperties.  # noqa: E501


        :return: The title of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this IdentifyPayloadProperties.


        :param title: The title of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def organization(self):
        """Gets the organization of this IdentifyPayloadProperties.  # noqa: E501


        :return: The organization of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this IdentifyPayloadProperties.


        :param organization: The organization of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._organization = organization

    @property
    def city(self):
        """Gets the city of this IdentifyPayloadProperties.  # noqa: E501


        :return: The city of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this IdentifyPayloadProperties.


        :param city: The city of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def region(self):
        """Gets the region of this IdentifyPayloadProperties.  # noqa: E501


        :return: The region of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this IdentifyPayloadProperties.


        :param region: The region of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def country(self):
        """Gets the country of this IdentifyPayloadProperties.  # noqa: E501


        :return: The country of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this IdentifyPayloadProperties.


        :param country: The country of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def zip(self):
        """Gets the zip of this IdentifyPayloadProperties.  # noqa: E501


        :return: The zip of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._zip

    @zip.setter
    def zip(self, zip):
        """Sets the zip of this IdentifyPayloadProperties.


        :param zip: The zip of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._zip = zip

    @property
    def image(self):
        """Gets the image of this IdentifyPayloadProperties.  # noqa: E501


        :return: The image of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this IdentifyPayloadProperties.


        :param image: The image of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._image = image

    @property
    def consent(self):
        """Gets the consent of this IdentifyPayloadProperties.  # noqa: E501


        :return: The consent of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: str
        """
        return self._consent

    @consent.setter
    def consent(self, consent):
        """Sets the consent of this IdentifyPayloadProperties.


        :param consent: The consent of this IdentifyPayloadProperties.  # noqa: E501
        :type: str
        """

        self._consent = consent

    @property
    def your_custom_field(self):
        """Gets the your_custom_field of this IdentifyPayloadProperties.  # noqa: E501


        :return: The your_custom_field of this IdentifyPayloadProperties.  # noqa: E501
        :rtype: OneOfidentifyPayloadPropertiesYourCustomField
        """
        return self._your_custom_field

    @your_custom_field.setter
    def your_custom_field(self, your_custom_field):
        """Sets the your_custom_field of this IdentifyPayloadProperties.


        :param your_custom_field: The your_custom_field of this IdentifyPayloadProperties.  # noqa: E501
        :type: OneOfidentifyPayloadPropertiesYourCustomField
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
        if issubclass(IdentifyPayloadProperties, dict):
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
        if not isinstance(other, IdentifyPayloadProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
