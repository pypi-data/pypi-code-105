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


class ProductFreight(object):
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
        'barcode': 'str',
        'sku_number': 'str',
        'brand': 'str',
        'name': 'str',
        'name_cn': 'str',
        'hs_code': 'str',
        'model': 'str',
        'customs_unit_code_weight': 'str',
        'customs_unit_code': 'str',
        'customs_unit_code_package': 'str',
        'country_of_origin': 'str',
        'net_weight': 'float',
        'gross_weight': 'float',
        'spec': 'str',
        'description_en': 'str',
        'description_cn': 'str',
        'additional_image_urls': 'list[str]',
        'store_ids': 'list[str]',
        'rrp_cny': 'float',
        'rrp_gbp': 'float',
        'customs_filing_id': 'str',
        'ingredients': 'str'
    }

    attribute_map = {
        'barcode': 'barcode',
        'sku_number': 'skuNumber',
        'brand': 'brand',
        'name': 'name',
        'name_cn': 'nameCn',
        'hs_code': 'hsCode',
        'model': 'model',
        'customs_unit_code_weight': 'customsUnitCodeWeight',
        'customs_unit_code': 'customsUnitCode',
        'customs_unit_code_package': 'customsUnitCodePackage',
        'country_of_origin': 'countryOfOrigin',
        'net_weight': 'netWeight',
        'gross_weight': 'grossWeight',
        'spec': 'spec',
        'description_en': 'descriptionEn',
        'description_cn': 'descriptionCn',
        'additional_image_urls': 'additionalImageUrls',
        'store_ids': 'storeIds',
        'rrp_cny': 'rrpCny',
        'rrp_gbp': 'rrpGbp',
        'customs_filing_id': 'customsFilingId',
        'ingredients': 'ingredients'
    }

    def __init__(self, barcode=None, sku_number=None, brand=None, name=None, name_cn=None, hs_code=None, model=None, customs_unit_code_weight=None, customs_unit_code=None, customs_unit_code_package=None, country_of_origin=None, net_weight=None, gross_weight=None, spec=None, description_en=None, description_cn=None, additional_image_urls=None, store_ids=None, rrp_cny=None, rrp_gbp=None, customs_filing_id=None, ingredients=None, local_vars_configuration=None):  # noqa: E501
        """ProductFreight - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._barcode = None
        self._sku_number = None
        self._brand = None
        self._name = None
        self._name_cn = None
        self._hs_code = None
        self._model = None
        self._customs_unit_code_weight = None
        self._customs_unit_code = None
        self._customs_unit_code_package = None
        self._country_of_origin = None
        self._net_weight = None
        self._gross_weight = None
        self._spec = None
        self._description_en = None
        self._description_cn = None
        self._additional_image_urls = None
        self._store_ids = None
        self._rrp_cny = None
        self._rrp_gbp = None
        self._customs_filing_id = None
        self._ingredients = None
        self.discriminator = None

        self.barcode = barcode
        self.sku_number = sku_number
        self.brand = brand
        self.name = name
        self.name_cn = name_cn
        self.hs_code = hs_code
        if model is not None:
            self.model = model
        self.customs_unit_code_weight = customs_unit_code_weight
        if customs_unit_code is not None:
            self.customs_unit_code = customs_unit_code
        self.customs_unit_code_package = customs_unit_code_package
        self.country_of_origin = country_of_origin
        self.net_weight = net_weight
        if gross_weight is not None:
            self.gross_weight = gross_weight
        if spec is not None:
            self.spec = spec
        if description_en is not None:
            self.description_en = description_en
        if description_cn is not None:
            self.description_cn = description_cn
        if additional_image_urls is not None:
            self.additional_image_urls = additional_image_urls
        if store_ids is not None:
            self.store_ids = store_ids
        if rrp_cny is not None:
            self.rrp_cny = rrp_cny
        if rrp_gbp is not None:
            self.rrp_gbp = rrp_gbp
        if customs_filing_id is not None:
            self.customs_filing_id = customs_filing_id
        if ingredients is not None:
            self.ingredients = ingredients

    @property
    def barcode(self):
        """Gets the barcode of this ProductFreight.  # noqa: E501

        The barcode of product  # noqa: E501

        :return: The barcode of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._barcode

    @barcode.setter
    def barcode(self, barcode):
        """Sets the barcode of this ProductFreight.

        The barcode of product  # noqa: E501

        :param barcode: The barcode of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and barcode is None:  # noqa: E501
            raise ValueError("Invalid value for `barcode`, must not be `None`")  # noqa: E501

        self._barcode = barcode

    @property
    def sku_number(self):
        """Gets the sku_number of this ProductFreight.  # noqa: E501

        The number of stock keeping unit  # noqa: E501

        :return: The sku_number of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._sku_number

    @sku_number.setter
    def sku_number(self, sku_number):
        """Sets the sku_number of this ProductFreight.

        The number of stock keeping unit  # noqa: E501

        :param sku_number: The sku_number of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and sku_number is None:  # noqa: E501
            raise ValueError("Invalid value for `sku_number`, must not be `None`")  # noqa: E501

        self._sku_number = sku_number

    @property
    def brand(self):
        """Gets the brand of this ProductFreight.  # noqa: E501

        The brand name of current product  # noqa: E501

        :return: The brand of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this ProductFreight.

        The brand name of current product  # noqa: E501

        :param brand: The brand of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and brand is None:  # noqa: E501
            raise ValueError("Invalid value for `brand`, must not be `None`")  # noqa: E501

        self._brand = brand

    @property
    def name(self):
        """Gets the name of this ProductFreight.  # noqa: E501

        The product name  # noqa: E501

        :return: The name of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ProductFreight.

        The product name  # noqa: E501

        :param name: The name of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def name_cn(self):
        """Gets the name_cn of this ProductFreight.  # noqa: E501

        Chinese name of product  # noqa: E501

        :return: The name_cn of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._name_cn

    @name_cn.setter
    def name_cn(self, name_cn):
        """Sets the name_cn of this ProductFreight.

        Chinese name of product  # noqa: E501

        :param name_cn: The name_cn of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name_cn is None:  # noqa: E501
            raise ValueError("Invalid value for `name_cn`, must not be `None`")  # noqa: E501

        self._name_cn = name_cn

    @property
    def hs_code(self):
        """Gets the hs_code of this ProductFreight.  # noqa: E501

        The Harmonized Commodity Description and Coding System (HS code) of the tariff nomenclature is an international standardised system of names and numbers for the classification of commodities  # noqa: E501

        :return: The hs_code of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._hs_code

    @hs_code.setter
    def hs_code(self, hs_code):
        """Sets the hs_code of this ProductFreight.

        The Harmonized Commodity Description and Coding System (HS code) of the tariff nomenclature is an international standardised system of names and numbers for the classification of commodities  # noqa: E501

        :param hs_code: The hs_code of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and hs_code is None:  # noqa: E501
            raise ValueError("Invalid value for `hs_code`, must not be `None`")  # noqa: E501

        self._hs_code = hs_code

    @property
    def model(self):
        """Gets the model of this ProductFreight.  # noqa: E501

        The model of current product.  # noqa: E501

        :return: The model of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this ProductFreight.

        The model of current product.  # noqa: E501

        :param model: The model of this ProductFreight.  # noqa: E501
        :type: str
        """

        self._model = model

    @property
    def customs_unit_code_weight(self):
        """Gets the customs_unit_code_weight of this ProductFreight.  # noqa: E501

        Legal first unit of measurement for customs product  # noqa: E501

        :return: The customs_unit_code_weight of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._customs_unit_code_weight

    @customs_unit_code_weight.setter
    def customs_unit_code_weight(self, customs_unit_code_weight):
        """Sets the customs_unit_code_weight of this ProductFreight.

        Legal first unit of measurement for customs product  # noqa: E501

        :param customs_unit_code_weight: The customs_unit_code_weight of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and customs_unit_code_weight is None:  # noqa: E501
            raise ValueError("Invalid value for `customs_unit_code_weight`, must not be `None`")  # noqa: E501

        self._customs_unit_code_weight = customs_unit_code_weight

    @property
    def customs_unit_code(self):
        """Gets the customs_unit_code of this ProductFreight.  # noqa: E501

        Legal second unit of measurement for customs product  # noqa: E501

        :return: The customs_unit_code of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._customs_unit_code

    @customs_unit_code.setter
    def customs_unit_code(self, customs_unit_code):
        """Sets the customs_unit_code of this ProductFreight.

        Legal second unit of measurement for customs product  # noqa: E501

        :param customs_unit_code: The customs_unit_code of this ProductFreight.  # noqa: E501
        :type: str
        """

        self._customs_unit_code = customs_unit_code

    @property
    def customs_unit_code_package(self):
        """Gets the customs_unit_code_package of this ProductFreight.  # noqa: E501

        The quantity unit code customs purpose. Declaration Unit  # noqa: E501

        :return: The customs_unit_code_package of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._customs_unit_code_package

    @customs_unit_code_package.setter
    def customs_unit_code_package(self, customs_unit_code_package):
        """Sets the customs_unit_code_package of this ProductFreight.

        The quantity unit code customs purpose. Declaration Unit  # noqa: E501

        :param customs_unit_code_package: The customs_unit_code_package of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and customs_unit_code_package is None:  # noqa: E501
            raise ValueError("Invalid value for `customs_unit_code_package`, must not be `None`")  # noqa: E501

        self._customs_unit_code_package = customs_unit_code_package

    @property
    def country_of_origin(self):
        """Gets the country_of_origin of this ProductFreight.  # noqa: E501

        Country of origin of of product  # noqa: E501

        :return: The country_of_origin of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._country_of_origin

    @country_of_origin.setter
    def country_of_origin(self, country_of_origin):
        """Sets the country_of_origin of this ProductFreight.

        Country of origin of of product  # noqa: E501

        :param country_of_origin: The country_of_origin of this ProductFreight.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and country_of_origin is None:  # noqa: E501
            raise ValueError("Invalid value for `country_of_origin`, must not be `None`")  # noqa: E501

        self._country_of_origin = country_of_origin

    @property
    def net_weight(self):
        """Gets the net_weight of this ProductFreight.  # noqa: E501

        Use Kilogram as the basic unit of mass  # noqa: E501

        :return: The net_weight of this ProductFreight.  # noqa: E501
        :rtype: float
        """
        return self._net_weight

    @net_weight.setter
    def net_weight(self, net_weight):
        """Sets the net_weight of this ProductFreight.

        Use Kilogram as the basic unit of mass  # noqa: E501

        :param net_weight: The net_weight of this ProductFreight.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and net_weight is None:  # noqa: E501
            raise ValueError("Invalid value for `net_weight`, must not be `None`")  # noqa: E501

        self._net_weight = net_weight

    @property
    def gross_weight(self):
        """Gets the gross_weight of this ProductFreight.  # noqa: E501

        Use Kilogram as the basic unit of mass  # noqa: E501

        :return: The gross_weight of this ProductFreight.  # noqa: E501
        :rtype: float
        """
        return self._gross_weight

    @gross_weight.setter
    def gross_weight(self, gross_weight):
        """Sets the gross_weight of this ProductFreight.

        Use Kilogram as the basic unit of mass  # noqa: E501

        :param gross_weight: The gross_weight of this ProductFreight.  # noqa: E501
        :type: float
        """

        self._gross_weight = gross_weight

    @property
    def spec(self):
        """Gets the spec of this ProductFreight.  # noqa: E501

        The spec of current product  # noqa: E501

        :return: The spec of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """Sets the spec of this ProductFreight.

        The spec of current product  # noqa: E501

        :param spec: The spec of this ProductFreight.  # noqa: E501
        :type: str
        """

        self._spec = spec

    @property
    def description_en(self):
        """Gets the description_en of this ProductFreight.  # noqa: E501

        The description of product  # noqa: E501

        :return: The description_en of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._description_en

    @description_en.setter
    def description_en(self, description_en):
        """Sets the description_en of this ProductFreight.

        The description of product  # noqa: E501

        :param description_en: The description_en of this ProductFreight.  # noqa: E501
        :type: str
        """

        self._description_en = description_en

    @property
    def description_cn(self):
        """Gets the description_cn of this ProductFreight.  # noqa: E501

        Chinese description of product  # noqa: E501

        :return: The description_cn of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._description_cn

    @description_cn.setter
    def description_cn(self, description_cn):
        """Sets the description_cn of this ProductFreight.

        Chinese description of product  # noqa: E501

        :param description_cn: The description_cn of this ProductFreight.  # noqa: E501
        :type: str
        """

        self._description_cn = description_cn

    @property
    def additional_image_urls(self):
        """Gets the additional_image_urls of this ProductFreight.  # noqa: E501

        Additional image urls  # noqa: E501

        :return: The additional_image_urls of this ProductFreight.  # noqa: E501
        :rtype: list[str]
        """
        return self._additional_image_urls

    @additional_image_urls.setter
    def additional_image_urls(self, additional_image_urls):
        """Sets the additional_image_urls of this ProductFreight.

        Additional image urls  # noqa: E501

        :param additional_image_urls: The additional_image_urls of this ProductFreight.  # noqa: E501
        :type: list[str]
        """

        self._additional_image_urls = additional_image_urls

    @property
    def store_ids(self):
        """Gets the store_ids of this ProductFreight.  # noqa: E501

        Available store ids of product  # noqa: E501

        :return: The store_ids of this ProductFreight.  # noqa: E501
        :rtype: list[str]
        """
        return self._store_ids

    @store_ids.setter
    def store_ids(self, store_ids):
        """Sets the store_ids of this ProductFreight.

        Available store ids of product  # noqa: E501

        :param store_ids: The store_ids of this ProductFreight.  # noqa: E501
        :type: list[str]
        """

        self._store_ids = store_ids

    @property
    def rrp_cny(self):
        """Gets the rrp_cny of this ProductFreight.  # noqa: E501

        Recommended retail price, unit is China Yuan  # noqa: E501

        :return: The rrp_cny of this ProductFreight.  # noqa: E501
        :rtype: float
        """
        return self._rrp_cny

    @rrp_cny.setter
    def rrp_cny(self, rrp_cny):
        """Sets the rrp_cny of this ProductFreight.

        Recommended retail price, unit is China Yuan  # noqa: E501

        :param rrp_cny: The rrp_cny of this ProductFreight.  # noqa: E501
        :type: float
        """

        self._rrp_cny = rrp_cny

    @property
    def rrp_gbp(self):
        """Gets the rrp_gbp of this ProductFreight.  # noqa: E501

        Recommended retail price, unit is Great Britain Pound  # noqa: E501

        :return: The rrp_gbp of this ProductFreight.  # noqa: E501
        :rtype: float
        """
        return self._rrp_gbp

    @rrp_gbp.setter
    def rrp_gbp(self, rrp_gbp):
        """Sets the rrp_gbp of this ProductFreight.

        Recommended retail price, unit is Great Britain Pound  # noqa: E501

        :param rrp_gbp: The rrp_gbp of this ProductFreight.  # noqa: E501
        :type: float
        """

        self._rrp_gbp = rrp_gbp

    @property
    def customs_filing_id(self):
        """Gets the customs_filing_id of this ProductFreight.  # noqa: E501

        The returned filing id of current SKU from customs  # noqa: E501

        :return: The customs_filing_id of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._customs_filing_id

    @customs_filing_id.setter
    def customs_filing_id(self, customs_filing_id):
        """Sets the customs_filing_id of this ProductFreight.

        The returned filing id of current SKU from customs  # noqa: E501

        :param customs_filing_id: The customs_filing_id of this ProductFreight.  # noqa: E501
        :type: str
        """

        self._customs_filing_id = customs_filing_id

    @property
    def ingredients(self):
        """Gets the ingredients of this ProductFreight.  # noqa: E501

        The ingredients of current product.  # noqa: E501

        :return: The ingredients of this ProductFreight.  # noqa: E501
        :rtype: str
        """
        return self._ingredients

    @ingredients.setter
    def ingredients(self, ingredients):
        """Sets the ingredients of this ProductFreight.

        The ingredients of current product.  # noqa: E501

        :param ingredients: The ingredients of this ProductFreight.  # noqa: E501
        :type: str
        """

        self._ingredients = ingredients

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
        if not isinstance(other, ProductFreight):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ProductFreight):
            return True

        return self.to_dict() != other.to_dict()
