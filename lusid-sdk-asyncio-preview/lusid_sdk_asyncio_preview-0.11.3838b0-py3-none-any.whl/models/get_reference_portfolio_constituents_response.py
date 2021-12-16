# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.3838
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid_asyncio.configuration import Configuration


class GetReferencePortfolioConstituentsResponse(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'effective_from': 'datetime',
        'weight_type': 'str',
        'period_type': 'str',
        'period_count': 'int',
        'constituents': 'list[ReferencePortfolioConstituent]',
        'href': 'str',
        'links': 'list[Link]'
    }

    attribute_map = {
        'effective_from': 'effectiveFrom',
        'weight_type': 'weightType',
        'period_type': 'periodType',
        'period_count': 'periodCount',
        'constituents': 'constituents',
        'href': 'href',
        'links': 'links'
    }

    required_map = {
        'effective_from': 'required',
        'weight_type': 'required',
        'period_type': 'optional',
        'period_count': 'optional',
        'constituents': 'required',
        'href': 'optional',
        'links': 'optional'
    }

    def __init__(self, effective_from=None, weight_type=None, period_type=None, period_count=None, constituents=None, href=None, links=None, local_vars_configuration=None):  # noqa: E501
        """GetReferencePortfolioConstituentsResponse - a model defined in OpenAPI"
        
        :param effective_from:  (required)
        :type effective_from: datetime
        :param weight_type:  The available values are: Static, Floating, Periodical (required)
        :type weight_type: str
        :param period_type:  The available values are: Daily, Weekly, Monthly, Quarterly, Annually
        :type period_type: str
        :param period_count: 
        :type period_count: int
        :param constituents:  Set of constituents (instrument/weight pairings) (required)
        :type constituents: list[lusid_asyncio.ReferencePortfolioConstituent]
        :param href:  The Uri that returns the same result as the original request,  but may include resolved as at time(s).
        :type href: str
        :param links:  Collection of links.
        :type links: list[lusid_asyncio.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._effective_from = None
        self._weight_type = None
        self._period_type = None
        self._period_count = None
        self._constituents = None
        self._href = None
        self._links = None
        self.discriminator = None

        self.effective_from = effective_from
        self.weight_type = weight_type
        self.period_type = period_type
        self.period_count = period_count
        self.constituents = constituents
        self.href = href
        self.links = links

    @property
    def effective_from(self):
        """Gets the effective_from of this GetReferencePortfolioConstituentsResponse.  # noqa: E501


        :return: The effective_from of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_from

    @effective_from.setter
    def effective_from(self, effective_from):
        """Sets the effective_from of this GetReferencePortfolioConstituentsResponse.


        :param effective_from: The effective_from of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :type effective_from: datetime
        """
        if self.local_vars_configuration.client_side_validation and effective_from is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_from`, must not be `None`")  # noqa: E501

        self._effective_from = effective_from

    @property
    def weight_type(self):
        """Gets the weight_type of this GetReferencePortfolioConstituentsResponse.  # noqa: E501

        The available values are: Static, Floating, Periodical  # noqa: E501

        :return: The weight_type of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :rtype: str
        """
        return self._weight_type

    @weight_type.setter
    def weight_type(self, weight_type):
        """Sets the weight_type of this GetReferencePortfolioConstituentsResponse.

        The available values are: Static, Floating, Periodical  # noqa: E501

        :param weight_type: The weight_type of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :type weight_type: str
        """
        if self.local_vars_configuration.client_side_validation and weight_type is None:  # noqa: E501
            raise ValueError("Invalid value for `weight_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Static", "Floating", "Periodical"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and weight_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `weight_type` ({0}), must be one of {1}"  # noqa: E501
                .format(weight_type, allowed_values)
            )

        self._weight_type = weight_type

    @property
    def period_type(self):
        """Gets the period_type of this GetReferencePortfolioConstituentsResponse.  # noqa: E501

        The available values are: Daily, Weekly, Monthly, Quarterly, Annually  # noqa: E501

        :return: The period_type of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :rtype: str
        """
        return self._period_type

    @period_type.setter
    def period_type(self, period_type):
        """Sets the period_type of this GetReferencePortfolioConstituentsResponse.

        The available values are: Daily, Weekly, Monthly, Quarterly, Annually  # noqa: E501

        :param period_type: The period_type of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :type period_type: str
        """
        allowed_values = [None,"Daily", "Weekly", "Monthly", "Quarterly", "Annually"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and period_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `period_type` ({0}), must be one of {1}"  # noqa: E501
                .format(period_type, allowed_values)
            )

        self._period_type = period_type

    @property
    def period_count(self):
        """Gets the period_count of this GetReferencePortfolioConstituentsResponse.  # noqa: E501


        :return: The period_count of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :rtype: int
        """
        return self._period_count

    @period_count.setter
    def period_count(self, period_count):
        """Sets the period_count of this GetReferencePortfolioConstituentsResponse.


        :param period_count: The period_count of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :type period_count: int
        """

        self._period_count = period_count

    @property
    def constituents(self):
        """Gets the constituents of this GetReferencePortfolioConstituentsResponse.  # noqa: E501

        Set of constituents (instrument/weight pairings)  # noqa: E501

        :return: The constituents of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :rtype: list[lusid_asyncio.ReferencePortfolioConstituent]
        """
        return self._constituents

    @constituents.setter
    def constituents(self, constituents):
        """Sets the constituents of this GetReferencePortfolioConstituentsResponse.

        Set of constituents (instrument/weight pairings)  # noqa: E501

        :param constituents: The constituents of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :type constituents: list[lusid_asyncio.ReferencePortfolioConstituent]
        """
        if self.local_vars_configuration.client_side_validation and constituents is None:  # noqa: E501
            raise ValueError("Invalid value for `constituents`, must not be `None`")  # noqa: E501

        self._constituents = constituents

    @property
    def href(self):
        """Gets the href of this GetReferencePortfolioConstituentsResponse.  # noqa: E501

        The Uri that returns the same result as the original request,  but may include resolved as at time(s).  # noqa: E501

        :return: The href of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this GetReferencePortfolioConstituentsResponse.

        The Uri that returns the same result as the original request,  but may include resolved as at time(s).  # noqa: E501

        :param href: The href of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def links(self):
        """Gets the links of this GetReferencePortfolioConstituentsResponse.  # noqa: E501

        Collection of links.  # noqa: E501

        :return: The links of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :rtype: list[lusid_asyncio.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this GetReferencePortfolioConstituentsResponse.

        Collection of links.  # noqa: E501

        :param links: The links of this GetReferencePortfolioConstituentsResponse.  # noqa: E501
        :type links: list[lusid_asyncio.Link]
        """

        self._links = links

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
        if not isinstance(other, GetReferencePortfolioConstituentsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetReferencePortfolioConstituentsResponse):
            return True

        return self.to_dict() != other.to_dict()
