# coding: utf-8

"""
    Nomad Pilot

    This is the API descriptor for the Nomad Pilot API, responsible for shipping and logistics processing. Developed by [Samarkand Global](https://www.samarkand.global/) in partnership with [SF Express](https://www.sf-express.com/), [eSinotrans](http://air.esinotrans.com/), [sto](http://sto-express.co.uk/). Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_pilot_cli` - Install for python with `pip install nomad-pilot-cli` - Install for Maven users `groupId, com.gitlab.samarkand-nomad; artifactId, nomad-pilot-cli`  # noqa: E501

    The version of the OpenAPI document: 1.44.21
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from nomad_pilot_cli.configuration import Configuration


class PackageFreight(object):
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
        'operation': 'str',
        'item_keys': 'list[str]',
        'page_no': 'int',
        'page_size': 'int'
    }

    attribute_map = {
        'operation': 'operation',
        'item_keys': 'itemKeys',
        'page_no': 'pageNo',
        'page_size': 'pageSize'
    }

    def __init__(self, operation='QUERY_WAYBILL', item_keys=[], page_no=None, page_size=None, local_vars_configuration=None):  # noqa: E501
        """PackageFreight - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._operation = None
        self._item_keys = None
        self._page_no = None
        self._page_size = None
        self.discriminator = None

        self.operation = operation
        if item_keys is not None:
            self.item_keys = item_keys
        if page_no is not None:
            self.page_no = page_no
        if page_size is not None:
            self.page_size = page_size

    @property
    def operation(self):
        """Gets the operation of this PackageFreight.  # noqa: E501

        Operation for Freight Forwarding DB, available options: QUERY, QUERY_PRODUCT, QUERY_WAYBILL. QUERY is deprecated  # noqa: E501

        :return: The operation of this PackageFreight.  # noqa: E501
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """Sets the operation of this PackageFreight.

        Operation for Freight Forwarding DB, available options: QUERY, QUERY_PRODUCT, QUERY_WAYBILL. QUERY is deprecated  # noqa: E501

        :param operation: The operation of this PackageFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and operation is None:  # noqa: E501
            raise ValueError("Invalid value for `operation`, must not be `None`")  # noqa: E501

        self._operation = operation

    @property
    def item_keys(self):
        """Gets the item_keys of this PackageFreight.  # noqa: E501

        Item keys, the key value could be tracking reference(QUERY_WAYBILL) or product sku(QUERY_PRODUCT)  # noqa: E501

        :return: The item_keys of this PackageFreight.  # noqa: E501
        :rtype: list[str]
        """
        return self._item_keys

    @item_keys.setter
    def item_keys(self, item_keys):
        """Sets the item_keys of this PackageFreight.

        Item keys, the key value could be tracking reference(QUERY_WAYBILL) or product sku(QUERY_PRODUCT)  # noqa: E501

        :param item_keys: The item_keys of this PackageFreight.  # noqa: E501
        :type: list[str]
        """

        self._item_keys = item_keys

    @property
    def page_no(self):
        """Gets the page_no of this PackageFreight.  # noqa: E501

        Page number  # noqa: E501

        :return: The page_no of this PackageFreight.  # noqa: E501
        :rtype: int
        """
        return self._page_no

    @page_no.setter
    def page_no(self, page_no):
        """Sets the page_no of this PackageFreight.

        Page number  # noqa: E501

        :param page_no: The page_no of this PackageFreight.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                page_no is not None and page_no < 1):  # noqa: E501
            raise ValueError("Invalid value for `page_no`, must be a value greater than or equal to `1`")  # noqa: E501

        self._page_no = page_no

    @property
    def page_size(self):
        """Gets the page_size of this PackageFreight.  # noqa: E501

        Page size  # noqa: E501

        :return: The page_size of this PackageFreight.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this PackageFreight.

        Page size  # noqa: E501

        :param page_size: The page_size of this PackageFreight.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                page_size is not None and page_size > 100):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                page_size is not None and page_size < 1):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value greater than or equal to `1`")  # noqa: E501

        self._page_size = page_size

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PackageFreight):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PackageFreight):
            return True

        return self.to_dict() != other.to_dict()
