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


class Device(object):
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
        'bootstrap_release': 'Release',
        'cloudiot_device': 'CloudiotDevice',
        'cameras': 'list[Camera]',
        'dashboard_url': 'str',
        'printer_controllers': 'list[PrinterController]',
        'release_channel': 'ReleaseChannelEnum',
        'user': 'User',
        'last_task': 'Task',
        'active_tasks': 'list[Task]',
        'active_cameras': 'list[Camera]',
        'created_dt': 'datetime',
        'updated_dt': 'datetime',
        'hostname': 'str'
    }

    attribute_map = {
        'id': 'id',
        'bootstrap_release': 'bootstrap_release',
        'cloudiot_device': 'cloudiot_device',
        'cameras': 'cameras',
        'dashboard_url': 'dashboard_url',
        'printer_controllers': 'printer_controllers',
        'release_channel': 'release_channel',
        'user': 'user',
        'last_task': 'last_task',
        'active_tasks': 'active_tasks',
        'active_cameras': 'active_cameras',
        'created_dt': 'created_dt',
        'updated_dt': 'updated_dt',
        'hostname': 'hostname'
    }

    def __init__(self, id=None, bootstrap_release=None, cloudiot_device=None, cameras=None, dashboard_url=None, printer_controllers=None, release_channel=None, user=None, last_task=None, active_tasks=None, active_cameras=None, created_dt=None, updated_dt=None, hostname=None, local_vars_configuration=None):  # noqa: E501
        """Device - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._bootstrap_release = None
        self._cloudiot_device = None
        self._cameras = None
        self._dashboard_url = None
        self._printer_controllers = None
        self._release_channel = None
        self._user = None
        self._last_task = None
        self._active_tasks = None
        self._active_cameras = None
        self._created_dt = None
        self._updated_dt = None
        self._hostname = None
        self.discriminator = None

        self.id = id
        self.bootstrap_release = bootstrap_release
        self.cloudiot_device = cloudiot_device
        self.cameras = cameras
        self.dashboard_url = dashboard_url
        self.printer_controllers = printer_controllers
        self.release_channel = release_channel
        self.user = user
        self.last_task = last_task
        self.active_tasks = active_tasks
        self.active_cameras = active_cameras
        self.created_dt = created_dt
        self.updated_dt = updated_dt
        if hostname is not None:
            self.hostname = hostname

    @property
    def id(self):
        """Gets the id of this Device.  # noqa: E501


        :return: The id of this Device.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Device.


        :param id: The id of this Device.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def bootstrap_release(self):
        """Gets the bootstrap_release of this Device.  # noqa: E501


        :return: The bootstrap_release of this Device.  # noqa: E501
        :rtype: Release
        """
        return self._bootstrap_release

    @bootstrap_release.setter
    def bootstrap_release(self, bootstrap_release):
        """Sets the bootstrap_release of this Device.


        :param bootstrap_release: The bootstrap_release of this Device.  # noqa: E501
        :type bootstrap_release: Release
        """

        self._bootstrap_release = bootstrap_release

    @property
    def cloudiot_device(self):
        """Gets the cloudiot_device of this Device.  # noqa: E501


        :return: The cloudiot_device of this Device.  # noqa: E501
        :rtype: CloudiotDevice
        """
        return self._cloudiot_device

    @cloudiot_device.setter
    def cloudiot_device(self, cloudiot_device):
        """Sets the cloudiot_device of this Device.


        :param cloudiot_device: The cloudiot_device of this Device.  # noqa: E501
        :type cloudiot_device: CloudiotDevice
        """

        self._cloudiot_device = cloudiot_device

    @property
    def cameras(self):
        """Gets the cameras of this Device.  # noqa: E501


        :return: The cameras of this Device.  # noqa: E501
        :rtype: list[Camera]
        """
        return self._cameras

    @cameras.setter
    def cameras(self, cameras):
        """Sets the cameras of this Device.


        :param cameras: The cameras of this Device.  # noqa: E501
        :type cameras: list[Camera]
        """
        if self.local_vars_configuration.client_side_validation and cameras is None:  # noqa: E501
            raise ValueError("Invalid value for `cameras`, must not be `None`")  # noqa: E501

        self._cameras = cameras

    @property
    def dashboard_url(self):
        """Gets the dashboard_url of this Device.  # noqa: E501


        :return: The dashboard_url of this Device.  # noqa: E501
        :rtype: str
        """
        return self._dashboard_url

    @dashboard_url.setter
    def dashboard_url(self, dashboard_url):
        """Sets the dashboard_url of this Device.


        :param dashboard_url: The dashboard_url of this Device.  # noqa: E501
        :type dashboard_url: str
        """
        if self.local_vars_configuration.client_side_validation and dashboard_url is None:  # noqa: E501
            raise ValueError("Invalid value for `dashboard_url`, must not be `None`")  # noqa: E501

        self._dashboard_url = dashboard_url

    @property
    def printer_controllers(self):
        """Gets the printer_controllers of this Device.  # noqa: E501


        :return: The printer_controllers of this Device.  # noqa: E501
        :rtype: list[PrinterController]
        """
        return self._printer_controllers

    @printer_controllers.setter
    def printer_controllers(self, printer_controllers):
        """Sets the printer_controllers of this Device.


        :param printer_controllers: The printer_controllers of this Device.  # noqa: E501
        :type printer_controllers: list[PrinterController]
        """
        if self.local_vars_configuration.client_side_validation and printer_controllers is None:  # noqa: E501
            raise ValueError("Invalid value for `printer_controllers`, must not be `None`")  # noqa: E501

        self._printer_controllers = printer_controllers

    @property
    def release_channel(self):
        """Gets the release_channel of this Device.  # noqa: E501


        :return: The release_channel of this Device.  # noqa: E501
        :rtype: ReleaseChannelEnum
        """
        return self._release_channel

    @release_channel.setter
    def release_channel(self, release_channel):
        """Sets the release_channel of this Device.


        :param release_channel: The release_channel of this Device.  # noqa: E501
        :type release_channel: ReleaseChannelEnum
        """

        self._release_channel = release_channel

    @property
    def user(self):
        """Gets the user of this Device.  # noqa: E501


        :return: The user of this Device.  # noqa: E501
        :rtype: User
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this Device.


        :param user: The user of this Device.  # noqa: E501
        :type user: User
        """

        self._user = user

    @property
    def last_task(self):
        """Gets the last_task of this Device.  # noqa: E501


        :return: The last_task of this Device.  # noqa: E501
        :rtype: Task
        """
        return self._last_task

    @last_task.setter
    def last_task(self, last_task):
        """Sets the last_task of this Device.


        :param last_task: The last_task of this Device.  # noqa: E501
        :type last_task: Task
        """

        self._last_task = last_task

    @property
    def active_tasks(self):
        """Gets the active_tasks of this Device.  # noqa: E501


        :return: The active_tasks of this Device.  # noqa: E501
        :rtype: list[Task]
        """
        return self._active_tasks

    @active_tasks.setter
    def active_tasks(self, active_tasks):
        """Sets the active_tasks of this Device.


        :param active_tasks: The active_tasks of this Device.  # noqa: E501
        :type active_tasks: list[Task]
        """
        if self.local_vars_configuration.client_side_validation and active_tasks is None:  # noqa: E501
            raise ValueError("Invalid value for `active_tasks`, must not be `None`")  # noqa: E501

        self._active_tasks = active_tasks

    @property
    def active_cameras(self):
        """Gets the active_cameras of this Device.  # noqa: E501


        :return: The active_cameras of this Device.  # noqa: E501
        :rtype: list[Camera]
        """
        return self._active_cameras

    @active_cameras.setter
    def active_cameras(self, active_cameras):
        """Sets the active_cameras of this Device.


        :param active_cameras: The active_cameras of this Device.  # noqa: E501
        :type active_cameras: list[Camera]
        """
        if self.local_vars_configuration.client_side_validation and active_cameras is None:  # noqa: E501
            raise ValueError("Invalid value for `active_cameras`, must not be `None`")  # noqa: E501

        self._active_cameras = active_cameras

    @property
    def created_dt(self):
        """Gets the created_dt of this Device.  # noqa: E501


        :return: The created_dt of this Device.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this Device.


        :param created_dt: The created_dt of this Device.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def updated_dt(self):
        """Gets the updated_dt of this Device.  # noqa: E501


        :return: The updated_dt of this Device.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this Device.


        :param updated_dt: The updated_dt of this Device.  # noqa: E501
        :type updated_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_dt`, must not be `None`")  # noqa: E501

        self._updated_dt = updated_dt

    @property
    def hostname(self):
        """Gets the hostname of this Device.  # noqa: E501

        Please enter the hostname you set in the Raspberry Pi Imager's Advanced Options menu (without .local extension)  # noqa: E501

        :return: The hostname of this Device.  # noqa: E501
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """Sets the hostname of this Device.

        Please enter the hostname you set in the Raspberry Pi Imager's Advanced Options menu (without .local extension)  # noqa: E501

        :param hostname: The hostname of this Device.  # noqa: E501
        :type hostname: str
        """
        if (self.local_vars_configuration.client_side_validation and
                hostname is not None and len(hostname) > 255):
            raise ValueError("Invalid value for `hostname`, length must be less than or equal to `255`")  # noqa: E501

        self._hostname = hostname

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
        if not isinstance(other, Device):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Device):
            return True

        return self.to_dict() != other.to_dict()
