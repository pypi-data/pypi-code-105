# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_1 import models

class HostPatch(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'add_iqns': 'list[str]',
        'add_nqns': 'list[str]',
        'add_wwns': 'list[str]',
        'chap': 'Chap',
        'host_group': 'ReferenceNoId',
        'iqns': 'list[str]',
        'nqns': 'list[str]',
        'personality': 'str',
        'preferred_arrays': 'list[Reference]',
        'remove_iqns': 'list[str]',
        'remove_nqns': 'list[str]',
        'remove_wwns': 'list[str]',
        'wwns': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'add_iqns': 'add_iqns',
        'add_nqns': 'add_nqns',
        'add_wwns': 'add_wwns',
        'chap': 'chap',
        'host_group': 'host_group',
        'iqns': 'iqns',
        'nqns': 'nqns',
        'personality': 'personality',
        'preferred_arrays': 'preferred_arrays',
        'remove_iqns': 'remove_iqns',
        'remove_nqns': 'remove_nqns',
        'remove_wwns': 'remove_wwns',
        'wwns': 'wwns'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        add_iqns=None,  # type: List[str]
        add_nqns=None,  # type: List[str]
        add_wwns=None,  # type: List[str]
        chap=None,  # type: models.Chap
        host_group=None,  # type: models.ReferenceNoId
        iqns=None,  # type: List[str]
        nqns=None,  # type: List[str]
        personality=None,  # type: str
        preferred_arrays=None,  # type: List[models.Reference]
        remove_iqns=None,  # type: List[str]
        remove_nqns=None,  # type: List[str]
        remove_wwns=None,  # type: List[str]
        wwns=None,  # type: List[str]
    ):
        """
        Keyword args:
            name (str): The new name for the resource.
            add_iqns (list[str]): Adds the specified iSCSI Qualified Names (IQNs) to those already associated with the specified host.
            add_nqns (list[str]): Adds the specified NVMe Qualified Names (NQNs) to those already associated with the specified host.
            add_wwns (list[str]): Adds the specified Fibre Channel World Wide Names (WWNs) to those already associated with the specified host.
            chap (Chap)
            host_group (ReferenceNoId): The host group to which the host should be associated.
            iqns (list[str]): The iSCSI qualified name (IQN) associated with the host.
            nqns (list[str]): The NVMe Qualified Name (NQN) associated with the host.
            personality (str): Determines how the system tunes the array to ensure that it works optimally with the host. Set `personality` to the name of the host operating system or virtual memory system. Valid values are `aix`, `esxi`, `hitachi-vsp`, `hpux`, `oracle-vm-server`, `solaris`, and `vms`. If your system is not listed as one of the valid host personalities, do not set the option. By default, the personality is not set.
            preferred_arrays (list[Reference]): For synchronous replication configurations, sets a host's preferred array to specify which array exposes active/optimized paths to that host. Enter multiple preferred arrays in comma-separated format. If a preferred array is set for a host, then the other arrays in the same pod will expose active/non-optimized paths to that host. If the host is in a host group, `preferred_arrays` cannot be set because host groups have their own preferred arrays. On a preferred array of a certain host, all the paths on all the ports (for both the primary and secondary controllers) are set up as A/O (active/optimized) paths, while on a non-preferred array, all the paths are A/N (Active/Non-optimized) paths.
            remove_iqns (list[str]): Disassociates the specified iSCSI Qualified Names (IQNs) from the specified host.
            remove_nqns (list[str]): Disassociates the specified NVMe Qualified Names (NQNs) from the specified host.
            remove_wwns (list[str]): Disassociates the specified Fibre Channel World Wide Names (WWNs) from the specified host.
            wwns (list[str]): The Fibre Channel World Wide Name (WWN) associated with the host.
        """
        if name is not None:
            self.name = name
        if add_iqns is not None:
            self.add_iqns = add_iqns
        if add_nqns is not None:
            self.add_nqns = add_nqns
        if add_wwns is not None:
            self.add_wwns = add_wwns
        if chap is not None:
            self.chap = chap
        if host_group is not None:
            self.host_group = host_group
        if iqns is not None:
            self.iqns = iqns
        if nqns is not None:
            self.nqns = nqns
        if personality is not None:
            self.personality = personality
        if preferred_arrays is not None:
            self.preferred_arrays = preferred_arrays
        if remove_iqns is not None:
            self.remove_iqns = remove_iqns
        if remove_nqns is not None:
            self.remove_nqns = remove_nqns
        if remove_wwns is not None:
            self.remove_wwns = remove_wwns
        if wwns is not None:
            self.wwns = wwns

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `HostPatch`".format(key))
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
        if issubclass(HostPatch, dict):
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
        if not isinstance(other, HostPatch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
