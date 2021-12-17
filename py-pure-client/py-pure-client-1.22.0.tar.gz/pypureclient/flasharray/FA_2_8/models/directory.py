# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.8
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_8 import models

class Directory(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'name': 'str',
        'created': 'int',
        'destroyed': 'bool',
        'directory_name': 'str',
        'file_system': 'FixedReference',
        'path': 'str',
        'space': 'Space',
        'time_remaining': 'int',
        'limited_by': 'LimitedBy'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'created': 'created',
        'destroyed': 'destroyed',
        'directory_name': 'directory_name',
        'file_system': 'file_system',
        'path': 'path',
        'space': 'space',
        'time_remaining': 'time_remaining',
        'limited_by': 'limited_by'
    }

    required_args = {
    }

    def __init__(
        self,
        id=None,  # type: str
        name=None,  # type: str
        created=None,  # type: int
        destroyed=None,  # type: bool
        directory_name=None,  # type: str
        file_system=None,  # type: models.FixedReference
        path=None,  # type: str
        space=None,  # type: models.Space
        time_remaining=None,  # type: int
        limited_by=None,  # type: models.LimitedBy
    ):
        """
        Keyword args:
            id (str): A globally unique, system-generated ID. The ID cannot be modified and cannot refer to another resource.
            name (str): A user-specified name. The name must be locally unique and can be changed.
            created (int): The managed directory creation time, measured in milliseconds since the UNIX epoch.
            destroyed (bool): Returns a value of `true` if the managed directory has been destroyed and is pending eradication. The `time_remaining` value displays the amount of time left until the destroyed managed directory is permanently eradicated. Once the `time_remaining` period has elapsed, the managed directory is permanently eradicated and can no longer be recovered.
            directory_name (str): The managed directory name without the file system name prefix. A full managed directory name is constructed in the form of `FILE_SYSTEM:DIR` where `FILE_SYSTEM` is the file system name and `DIR` is the value of this field.
            file_system (FixedReference): The file system that this managed directory is in.
            path (str): Absolute path of the managed directory in the file system.
            space (Space): Displays size and space consumption information.
            time_remaining (int): The amount of time left, measured in milliseconds until the destroyed managed directory is permanently eradicated.
            limited_by (LimitedBy): The quota policy that is limiting usage on this managed directory. This policy defines the total amount of space provisioned to this managed directory and its descendants. The returned value contains two parts&#58; the name of the policy and the managed directory to which the policy is attached.
        """
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if created is not None:
            self.created = created
        if destroyed is not None:
            self.destroyed = destroyed
        if directory_name is not None:
            self.directory_name = directory_name
        if file_system is not None:
            self.file_system = file_system
        if path is not None:
            self.path = path
        if space is not None:
            self.space = space
        if time_remaining is not None:
            self.time_remaining = time_remaining
        if limited_by is not None:
            self.limited_by = limited_by

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Directory`".format(key))
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
        if issubclass(Directory, dict):
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
        if not isinstance(other, Directory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
