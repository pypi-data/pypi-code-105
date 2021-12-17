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


class RemoteControlCommand(object):
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
        'created_dt': 'datetime',
        'command': 'CommandEnum',
        'user': 'int',
        'device': 'int',
        'received': 'bool',
        'success': 'bool',
        'iotcore_response': 'dict(str, object)',
        'metadata': 'dict(str, object)',
        'url': 'str',
        'octoprint_event_type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'created_dt': 'created_dt',
        'command': 'command',
        'user': 'user',
        'device': 'device',
        'received': 'received',
        'success': 'success',
        'iotcore_response': 'iotcore_response',
        'metadata': 'metadata',
        'url': 'url',
        'octoprint_event_type': 'octoprint_event_type'
    }

    def __init__(self, id=None, created_dt=None, command=None, user=None, device=None, received=None, success=None, iotcore_response=None, metadata=None, url=None, octoprint_event_type=None, local_vars_configuration=None):  # noqa: E501
        """RemoteControlCommand - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._created_dt = None
        self._command = None
        self._user = None
        self._device = None
        self._received = None
        self._success = None
        self._iotcore_response = None
        self._metadata = None
        self._url = None
        self._octoprint_event_type = None
        self.discriminator = None

        self.id = id
        self.created_dt = created_dt
        if command is not None:
            self.command = command
        self.user = user
        self.device = device
        if received is not None:
            self.received = received
        self.success = success
        if iotcore_response is not None:
            self.iotcore_response = iotcore_response
        if metadata is not None:
            self.metadata = metadata
        self.url = url
        self.octoprint_event_type = octoprint_event_type

    @property
    def id(self):
        """Gets the id of this RemoteControlCommand.  # noqa: E501


        :return: The id of this RemoteControlCommand.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RemoteControlCommand.


        :param id: The id of this RemoteControlCommand.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_dt(self):
        """Gets the created_dt of this RemoteControlCommand.  # noqa: E501


        :return: The created_dt of this RemoteControlCommand.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this RemoteControlCommand.


        :param created_dt: The created_dt of this RemoteControlCommand.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def command(self):
        """Gets the command of this RemoteControlCommand.  # noqa: E501


        :return: The command of this RemoteControlCommand.  # noqa: E501
        :rtype: CommandEnum
        """
        return self._command

    @command.setter
    def command(self, command):
        """Sets the command of this RemoteControlCommand.


        :param command: The command of this RemoteControlCommand.  # noqa: E501
        :type command: CommandEnum
        """

        self._command = command

    @property
    def user(self):
        """Gets the user of this RemoteControlCommand.  # noqa: E501


        :return: The user of this RemoteControlCommand.  # noqa: E501
        :rtype: int
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this RemoteControlCommand.


        :param user: The user of this RemoteControlCommand.  # noqa: E501
        :type user: int
        """
        if self.local_vars_configuration.client_side_validation and user is None:  # noqa: E501
            raise ValueError("Invalid value for `user`, must not be `None`")  # noqa: E501

        self._user = user

    @property
    def device(self):
        """Gets the device of this RemoteControlCommand.  # noqa: E501


        :return: The device of this RemoteControlCommand.  # noqa: E501
        :rtype: int
        """
        return self._device

    @device.setter
    def device(self, device):
        """Sets the device of this RemoteControlCommand.


        :param device: The device of this RemoteControlCommand.  # noqa: E501
        :type device: int
        """
        if self.local_vars_configuration.client_side_validation and device is None:  # noqa: E501
            raise ValueError("Invalid value for `device`, must not be `None`")  # noqa: E501

        self._device = device

    @property
    def received(self):
        """Gets the received of this RemoteControlCommand.  # noqa: E501


        :return: The received of this RemoteControlCommand.  # noqa: E501
        :rtype: bool
        """
        return self._received

    @received.setter
    def received(self, received):
        """Sets the received of this RemoteControlCommand.


        :param received: The received of this RemoteControlCommand.  # noqa: E501
        :type received: bool
        """

        self._received = received

    @property
    def success(self):
        """Gets the success of this RemoteControlCommand.  # noqa: E501


        :return: The success of this RemoteControlCommand.  # noqa: E501
        :rtype: bool
        """
        return self._success

    @success.setter
    def success(self, success):
        """Sets the success of this RemoteControlCommand.


        :param success: The success of this RemoteControlCommand.  # noqa: E501
        :type success: bool
        """

        self._success = success

    @property
    def iotcore_response(self):
        """Gets the iotcore_response of this RemoteControlCommand.  # noqa: E501


        :return: The iotcore_response of this RemoteControlCommand.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._iotcore_response

    @iotcore_response.setter
    def iotcore_response(self, iotcore_response):
        """Sets the iotcore_response of this RemoteControlCommand.


        :param iotcore_response: The iotcore_response of this RemoteControlCommand.  # noqa: E501
        :type iotcore_response: dict(str, object)
        """

        self._iotcore_response = iotcore_response

    @property
    def metadata(self):
        """Gets the metadata of this RemoteControlCommand.  # noqa: E501


        :return: The metadata of this RemoteControlCommand.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this RemoteControlCommand.


        :param metadata: The metadata of this RemoteControlCommand.  # noqa: E501
        :type metadata: dict(str, object)
        """

        self._metadata = metadata

    @property
    def url(self):
        """Gets the url of this RemoteControlCommand.  # noqa: E501


        :return: The url of this RemoteControlCommand.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this RemoteControlCommand.


        :param url: The url of this RemoteControlCommand.  # noqa: E501
        :type url: str
        """
        if self.local_vars_configuration.client_side_validation and url is None:  # noqa: E501
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def octoprint_event_type(self):
        """Gets the octoprint_event_type of this RemoteControlCommand.  # noqa: E501


        :return: The octoprint_event_type of this RemoteControlCommand.  # noqa: E501
        :rtype: str
        """
        return self._octoprint_event_type

    @octoprint_event_type.setter
    def octoprint_event_type(self, octoprint_event_type):
        """Sets the octoprint_event_type of this RemoteControlCommand.


        :param octoprint_event_type: The octoprint_event_type of this RemoteControlCommand.  # noqa: E501
        :type octoprint_event_type: str
        """
        if self.local_vars_configuration.client_side_validation and octoprint_event_type is None:  # noqa: E501
            raise ValueError("Invalid value for `octoprint_event_type`, must not be `None`")  # noqa: E501

        self._octoprint_event_type = octoprint_event_type

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
        if not isinstance(other, RemoteControlCommand):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RemoteControlCommand):
            return True

        return self.to_dict() != other.to_dict()
