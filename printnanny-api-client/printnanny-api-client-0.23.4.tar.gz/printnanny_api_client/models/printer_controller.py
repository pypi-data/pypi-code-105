# coding: utf-8

"""
    printnanny-api-client

    Official API client library for print-nanny.com  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Contact: leigh@print-nanny.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from printnanny_api_client.configuration import Configuration


class PrinterController(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'int',
        'software': 'SoftwareEnum',
        'created_dt': 'datetime',
        'updated_dt': 'datetime',
        'polymorphic_ctype': 'int',
        'user': 'int',
        'device': 'int'
    }

    attribute_map = {
        'id': 'id',
        'software': 'software',
        'created_dt': 'created_dt',
        'updated_dt': 'updated_dt',
        'polymorphic_ctype': 'polymorphic_ctype',
        'user': 'user',
        'device': 'device'
    }

    def __init__(self, id=None, software=None, created_dt=None, updated_dt=None, polymorphic_ctype=None, user=None, device=None, local_vars_configuration=None):  # noqa: E501
        """PrinterController - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._software = None
        self._created_dt = None
        self._updated_dt = None
        self._polymorphic_ctype = None
        self._user = None
        self._device = None
        self.discriminator = None

        self.id = id
        self.software = software
        self.created_dt = created_dt
        self.updated_dt = updated_dt
        self.polymorphic_ctype = polymorphic_ctype
        self.user = user
        self.device = device

    @property
    def id(self):
        """Gets the id of this PrinterController.  # noqa: E501


        :return: The id of this PrinterController.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PrinterController.


        :param id: The id of this PrinterController.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def software(self):
        """Gets the software of this PrinterController.  # noqa: E501


        :return: The software of this PrinterController.  # noqa: E501
        :rtype: SoftwareEnum
        """
        return self._software

    @software.setter
    def software(self, software):
        """Sets the software of this PrinterController.


        :param software: The software of this PrinterController.  # noqa: E501
        :type software: SoftwareEnum
        """

        self._software = software

    @property
    def created_dt(self):
        """Gets the created_dt of this PrinterController.  # noqa: E501


        :return: The created_dt of this PrinterController.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this PrinterController.


        :param created_dt: The created_dt of this PrinterController.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def updated_dt(self):
        """Gets the updated_dt of this PrinterController.  # noqa: E501


        :return: The updated_dt of this PrinterController.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this PrinterController.


        :param updated_dt: The updated_dt of this PrinterController.  # noqa: E501
        :type updated_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_dt`, must not be `None`")  # noqa: E501

        self._updated_dt = updated_dt

    @property
    def polymorphic_ctype(self):
        """Gets the polymorphic_ctype of this PrinterController.  # noqa: E501


        :return: The polymorphic_ctype of this PrinterController.  # noqa: E501
        :rtype: int
        """
        return self._polymorphic_ctype

    @polymorphic_ctype.setter
    def polymorphic_ctype(self, polymorphic_ctype):
        """Sets the polymorphic_ctype of this PrinterController.


        :param polymorphic_ctype: The polymorphic_ctype of this PrinterController.  # noqa: E501
        :type polymorphic_ctype: int
        """
        if self.local_vars_configuration.client_side_validation and polymorphic_ctype is None:  # noqa: E501
            raise ValueError("Invalid value for `polymorphic_ctype`, must not be `None`")  # noqa: E501

        self._polymorphic_ctype = polymorphic_ctype

    @property
    def user(self):
        """Gets the user of this PrinterController.  # noqa: E501


        :return: The user of this PrinterController.  # noqa: E501
        :rtype: int
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this PrinterController.


        :param user: The user of this PrinterController.  # noqa: E501
        :type user: int
        """
        if self.local_vars_configuration.client_side_validation and user is None:  # noqa: E501
            raise ValueError("Invalid value for `user`, must not be `None`")  # noqa: E501

        self._user = user

    @property
    def device(self):
        """Gets the device of this PrinterController.  # noqa: E501


        :return: The device of this PrinterController.  # noqa: E501
        :rtype: int
        """
        return self._device

    @device.setter
    def device(self, device):
        """Sets the device of this PrinterController.


        :param device: The device of this PrinterController.  # noqa: E501
        :type device: int
        """
        if self.local_vars_configuration.client_side_validation and device is None:  # noqa: E501
            raise ValueError("Invalid value for `device`, must not be `None`")  # noqa: E501

        self._device = device

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PrinterController):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PrinterController):
            return True

        return self.to_dict() != other.to_dict()
