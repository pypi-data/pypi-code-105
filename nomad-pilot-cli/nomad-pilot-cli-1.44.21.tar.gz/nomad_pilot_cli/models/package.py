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


class Package(object):
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
        'dimension': 'Dimension',
        'ship_from': 'AddressShip',
        'ship_to': 'AddressShip',
        'bill': 'Address',
        'order_ref': 'str',
        'seller_order_ref': 'str',
        'tracking_reference': 'str',
        'order_time': 'str',
        'gross_weight': 'float',
        'net_weight': 'float',
        'total_price': 'float',
        'currency': 'str',
        'mass_unit': 'str',
        'length_unit': 'str',
        'domestic_delivery_company': 'str',
        'created_at': 'str',
        'updated_at': 'str',
        'pay_method': 'str',
        'pay_merchant_name': 'str',
        'pay_amount': 'float',
        'pay_id': 'str',
        'paid_at': 'str',
        'products_total_tax': 'float',
        'shipping_cost': 'float',
        'non_cash_deduction_amount': 'float',
        'customer_note': 'str',
        'cancel_reason': 'str',
        'warehouse_code': 'str',
        'customer_id_ref': 'str',
        'insurance_fee': 'float',
        'express_type': 'str',
        'payment_pay_id': 'str',
        'platform_name': 'str',
        'check_point': 'str',
        'items': 'list[PackageItem]'
    }

    attribute_map = {
        'dimension': 'dimension',
        'ship_from': 'shipFrom',
        'ship_to': 'shipTo',
        'bill': 'bill',
        'order_ref': 'orderRef',
        'seller_order_ref': 'sellerOrderRef',
        'tracking_reference': 'trackingReference',
        'order_time': 'orderTime',
        'gross_weight': 'grossWeight',
        'net_weight': 'netWeight',
        'total_price': 'totalPrice',
        'currency': 'currency',
        'mass_unit': 'massUnit',
        'length_unit': 'lengthUnit',
        'domestic_delivery_company': 'domesticDeliveryCompany',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'pay_method': 'payMethod',
        'pay_merchant_name': 'payMerchantName',
        'pay_amount': 'payAmount',
        'pay_id': 'payId',
        'paid_at': 'paidAt',
        'products_total_tax': 'productsTotalTax',
        'shipping_cost': 'shippingCost',
        'non_cash_deduction_amount': 'nonCashDeductionAmount',
        'customer_note': 'customerNote',
        'cancel_reason': 'cancelReason',
        'warehouse_code': 'warehouseCode',
        'customer_id_ref': 'customerIdRef',
        'insurance_fee': 'insuranceFee',
        'express_type': 'expressType',
        'payment_pay_id': 'paymentPayId',
        'platform_name': 'platformName',
        'check_point': 'checkPoint',
        'items': 'items'
    }

    def __init__(self, dimension=None, ship_from=None, ship_to=None, bill=None, order_ref=None, seller_order_ref=None, tracking_reference=None, order_time=None, gross_weight=None, net_weight=None, total_price=None, currency='RMB', mass_unit='Kilogram', length_unit='Centimetre', domestic_delivery_company='SF', created_at=None, updated_at=None, pay_method=None, pay_merchant_name=None, pay_amount=None, pay_id=None, paid_at=None, products_total_tax=None, shipping_cost=None, non_cash_deduction_amount=None, customer_note=None, cancel_reason=None, warehouse_code=None, customer_id_ref=None, insurance_fee=None, express_type=None, payment_pay_id=None, platform_name='youzan', check_point=None, items=None, local_vars_configuration=None):  # noqa: E501
        """Package - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._dimension = None
        self._ship_from = None
        self._ship_to = None
        self._bill = None
        self._order_ref = None
        self._seller_order_ref = None
        self._tracking_reference = None
        self._order_time = None
        self._gross_weight = None
        self._net_weight = None
        self._total_price = None
        self._currency = None
        self._mass_unit = None
        self._length_unit = None
        self._domestic_delivery_company = None
        self._created_at = None
        self._updated_at = None
        self._pay_method = None
        self._pay_merchant_name = None
        self._pay_amount = None
        self._pay_id = None
        self._paid_at = None
        self._products_total_tax = None
        self._shipping_cost = None
        self._non_cash_deduction_amount = None
        self._customer_note = None
        self._cancel_reason = None
        self._warehouse_code = None
        self._customer_id_ref = None
        self._insurance_fee = None
        self._express_type = None
        self._payment_pay_id = None
        self._platform_name = None
        self._check_point = None
        self._items = None
        self.discriminator = None

        if dimension is not None:
            self.dimension = dimension
        if ship_from is not None:
            self.ship_from = ship_from
        if ship_to is not None:
            self.ship_to = ship_to
        if bill is not None:
            self.bill = bill
        if order_ref is not None:
            self.order_ref = order_ref
        self.seller_order_ref = seller_order_ref
        if tracking_reference is not None:
            self.tracking_reference = tracking_reference
        if order_time is not None:
            self.order_time = order_time
        if gross_weight is not None:
            self.gross_weight = gross_weight
        if net_weight is not None:
            self.net_weight = net_weight
        if total_price is not None:
            self.total_price = total_price
        self.currency = currency
        self.mass_unit = mass_unit
        self.length_unit = length_unit
        if domestic_delivery_company is not None:
            self.domestic_delivery_company = domestic_delivery_company
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if pay_method is not None:
            self.pay_method = pay_method
        if pay_merchant_name is not None:
            self.pay_merchant_name = pay_merchant_name
        if pay_amount is not None:
            self.pay_amount = pay_amount
        if pay_id is not None:
            self.pay_id = pay_id
        if paid_at is not None:
            self.paid_at = paid_at
        if products_total_tax is not None:
            self.products_total_tax = products_total_tax
        if shipping_cost is not None:
            self.shipping_cost = shipping_cost
        if non_cash_deduction_amount is not None:
            self.non_cash_deduction_amount = non_cash_deduction_amount
        if customer_note is not None:
            self.customer_note = customer_note
        if cancel_reason is not None:
            self.cancel_reason = cancel_reason
        if warehouse_code is not None:
            self.warehouse_code = warehouse_code
        if customer_id_ref is not None:
            self.customer_id_ref = customer_id_ref
        if insurance_fee is not None:
            self.insurance_fee = insurance_fee
        self.express_type = express_type
        if payment_pay_id is not None:
            self.payment_pay_id = payment_pay_id
        if platform_name is not None:
            self.platform_name = platform_name
        if check_point is not None:
            self.check_point = check_point
        if items is not None:
            self.items = items

    @property
    def dimension(self):
        """Gets the dimension of this Package.  # noqa: E501


        :return: The dimension of this Package.  # noqa: E501
        :rtype: Dimension
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        """Sets the dimension of this Package.


        :param dimension: The dimension of this Package.  # noqa: E501
        :type: Dimension
        """

        self._dimension = dimension

    @property
    def ship_from(self):
        """Gets the ship_from of this Package.  # noqa: E501


        :return: The ship_from of this Package.  # noqa: E501
        :rtype: AddressShip
        """
        return self._ship_from

    @ship_from.setter
    def ship_from(self, ship_from):
        """Sets the ship_from of this Package.


        :param ship_from: The ship_from of this Package.  # noqa: E501
        :type: AddressShip
        """

        self._ship_from = ship_from

    @property
    def ship_to(self):
        """Gets the ship_to of this Package.  # noqa: E501


        :return: The ship_to of this Package.  # noqa: E501
        :rtype: AddressShip
        """
        return self._ship_to

    @ship_to.setter
    def ship_to(self, ship_to):
        """Sets the ship_to of this Package.


        :param ship_to: The ship_to of this Package.  # noqa: E501
        :type: AddressShip
        """

        self._ship_to = ship_to

    @property
    def bill(self):
        """Gets the bill of this Package.  # noqa: E501


        :return: The bill of this Package.  # noqa: E501
        :rtype: Address
        """
        return self._bill

    @bill.setter
    def bill(self, bill):
        """Sets the bill of this Package.


        :param bill: The bill of this Package.  # noqa: E501
        :type: Address
        """

        self._bill = bill

    @property
    def order_ref(self):
        """Gets the order_ref of this Package.  # noqa: E501

        Order reference number in ERP application  # noqa: E501

        :return: The order_ref of this Package.  # noqa: E501
        :rtype: str
        """
        return self._order_ref

    @order_ref.setter
    def order_ref(self, order_ref):
        """Sets the order_ref of this Package.

        Order reference number in ERP application  # noqa: E501

        :param order_ref: The order_ref of this Package.  # noqa: E501
        :type: str
        """

        self._order_ref = order_ref

    @property
    def seller_order_ref(self):
        """Gets the seller_order_ref of this Package.  # noqa: E501


        :return: The seller_order_ref of this Package.  # noqa: E501
        :rtype: str
        """
        return self._seller_order_ref

    @seller_order_ref.setter
    def seller_order_ref(self, seller_order_ref):
        """Sets the seller_order_ref of this Package.


        :param seller_order_ref: The seller_order_ref of this Package.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and seller_order_ref is None:  # noqa: E501
            raise ValueError("Invalid value for `seller_order_ref`, must not be `None`")  # noqa: E501

        self._seller_order_ref = seller_order_ref

    @property
    def tracking_reference(self):
        """Gets the tracking_reference of this Package.  # noqa: E501

        Package tracking reference from logistics company  # noqa: E501

        :return: The tracking_reference of this Package.  # noqa: E501
        :rtype: str
        """
        return self._tracking_reference

    @tracking_reference.setter
    def tracking_reference(self, tracking_reference):
        """Sets the tracking_reference of this Package.

        Package tracking reference from logistics company  # noqa: E501

        :param tracking_reference: The tracking_reference of this Package.  # noqa: E501
        :type: str
        """

        self._tracking_reference = tracking_reference

    @property
    def order_time(self):
        """Gets the order_time of this Package.  # noqa: E501

        ISO 8601 format, '2019-01-19T18:30:52.442118+00:00' or '2019-01-19T18:30:52+00:00'  # noqa: E501

        :return: The order_time of this Package.  # noqa: E501
        :rtype: str
        """
        return self._order_time

    @order_time.setter
    def order_time(self, order_time):
        """Sets the order_time of this Package.

        ISO 8601 format, '2019-01-19T18:30:52.442118+00:00' or '2019-01-19T18:30:52+00:00'  # noqa: E501

        :param order_time: The order_time of this Package.  # noqa: E501
        :type: str
        """

        self._order_time = order_time

    @property
    def gross_weight(self):
        """Gets the gross_weight of this Package.  # noqa: E501

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :return: The gross_weight of this Package.  # noqa: E501
        :rtype: float
        """
        return self._gross_weight

    @gross_weight.setter
    def gross_weight(self, gross_weight):
        """Sets the gross_weight of this Package.

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :param gross_weight: The gross_weight of this Package.  # noqa: E501
        :type: float
        """

        self._gross_weight = gross_weight

    @property
    def net_weight(self):
        """Gets the net_weight of this Package.  # noqa: E501

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :return: The net_weight of this Package.  # noqa: E501
        :rtype: float
        """
        return self._net_weight

    @net_weight.setter
    def net_weight(self, net_weight):
        """Sets the net_weight of this Package.

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :param net_weight: The net_weight of this Package.  # noqa: E501
        :type: float
        """

        self._net_weight = net_weight

    @property
    def total_price(self):
        """Gets the total_price of this Package.  # noqa: E501

        The total price of this package, not including any discount and tax.  # noqa: E501

        :return: The total_price of this Package.  # noqa: E501
        :rtype: float
        """
        return self._total_price

    @total_price.setter
    def total_price(self, total_price):
        """Sets the total_price of this Package.

        The total price of this package, not including any discount and tax.  # noqa: E501

        :param total_price: The total_price of this Package.  # noqa: E501
        :type: float
        """

        self._total_price = total_price

    @property
    def currency(self):
        """Gets the currency of this Package.  # noqa: E501

        Price makes sense under an explicit currency, available options: RMB, CNY, USD, GBP  # noqa: E501

        :return: The currency of this Package.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Package.

        Price makes sense under an explicit currency, available options: RMB, CNY, USD, GBP  # noqa: E501

        :param currency: The currency of this Package.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and currency is None:  # noqa: E501
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501

        self._currency = currency

    @property
    def mass_unit(self):
        """Gets the mass_unit of this Package.  # noqa: E501


        :return: The mass_unit of this Package.  # noqa: E501
        :rtype: str
        """
        return self._mass_unit

    @mass_unit.setter
    def mass_unit(self, mass_unit):
        """Sets the mass_unit of this Package.


        :param mass_unit: The mass_unit of this Package.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and mass_unit is None:  # noqa: E501
            raise ValueError("Invalid value for `mass_unit`, must not be `None`")  # noqa: E501

        self._mass_unit = mass_unit

    @property
    def length_unit(self):
        """Gets the length_unit of this Package.  # noqa: E501


        :return: The length_unit of this Package.  # noqa: E501
        :rtype: str
        """
        return self._length_unit

    @length_unit.setter
    def length_unit(self, length_unit):
        """Sets the length_unit of this Package.


        :param length_unit: The length_unit of this Package.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and length_unit is None:  # noqa: E501
            raise ValueError("Invalid value for `length_unit`, must not be `None`")  # noqa: E501

        self._length_unit = length_unit

    @property
    def domestic_delivery_company(self):
        """Gets the domestic_delivery_company of this Package.  # noqa: E501

        the domestic delivery vendor, 2 available options: [SF, YTO]  # noqa: E501

        :return: The domestic_delivery_company of this Package.  # noqa: E501
        :rtype: str
        """
        return self._domestic_delivery_company

    @domestic_delivery_company.setter
    def domestic_delivery_company(self, domestic_delivery_company):
        """Sets the domestic_delivery_company of this Package.

        the domestic delivery vendor, 2 available options: [SF, YTO]  # noqa: E501

        :param domestic_delivery_company: The domestic_delivery_company of this Package.  # noqa: E501
        :type: str
        """

        self._domestic_delivery_company = domestic_delivery_company

    @property
    def created_at(self):
        """Gets the created_at of this Package.  # noqa: E501

        The time when current order was created. ISO_8601 format  # noqa: E501

        :return: The created_at of this Package.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Package.

        The time when current order was created. ISO_8601 format  # noqa: E501

        :param created_at: The created_at of this Package.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Package.  # noqa: E501

        The time when current order was updated. ISO_8601 format  # noqa: E501

        :return: The updated_at of this Package.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Package.

        The time when current order was updated. ISO_8601 format  # noqa: E501

        :param updated_at: The updated_at of this Package.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

    @property
    def pay_method(self):
        """Gets the pay_method of this Package.  # noqa: E501


        :return: The pay_method of this Package.  # noqa: E501
        :rtype: str
        """
        return self._pay_method

    @pay_method.setter
    def pay_method(self, pay_method):
        """Sets the pay_method of this Package.


        :param pay_method: The pay_method of this Package.  # noqa: E501
        :type: str
        """

        self._pay_method = pay_method

    @property
    def pay_merchant_name(self):
        """Gets the pay_merchant_name of this Package.  # noqa: E501


        :return: The pay_merchant_name of this Package.  # noqa: E501
        :rtype: str
        """
        return self._pay_merchant_name

    @pay_merchant_name.setter
    def pay_merchant_name(self, pay_merchant_name):
        """Sets the pay_merchant_name of this Package.


        :param pay_merchant_name: The pay_merchant_name of this Package.  # noqa: E501
        :type: str
        """

        self._pay_merchant_name = pay_merchant_name

    @property
    def pay_amount(self):
        """Gets the pay_amount of this Package.  # noqa: E501

        The actual amount paid for the order.  # noqa: E501

        :return: The pay_amount of this Package.  # noqa: E501
        :rtype: float
        """
        return self._pay_amount

    @pay_amount.setter
    def pay_amount(self, pay_amount):
        """Sets the pay_amount of this Package.

        The actual amount paid for the order.  # noqa: E501

        :param pay_amount: The pay_amount of this Package.  # noqa: E501
        :type: float
        """

        self._pay_amount = pay_amount

    @property
    def pay_id(self):
        """Gets the pay_id of this Package.  # noqa: E501

        The payment number generated by eCommerce platform such as Youzan  # noqa: E501

        :return: The pay_id of this Package.  # noqa: E501
        :rtype: str
        """
        return self._pay_id

    @pay_id.setter
    def pay_id(self, pay_id):
        """Sets the pay_id of this Package.

        The payment number generated by eCommerce platform such as Youzan  # noqa: E501

        :param pay_id: The pay_id of this Package.  # noqa: E501
        :type: str
        """

        self._pay_id = pay_id

    @property
    def paid_at(self):
        """Gets the paid_at of this Package.  # noqa: E501

        The time when the pay was made. ISO_8601 format  # noqa: E501

        :return: The paid_at of this Package.  # noqa: E501
        :rtype: str
        """
        return self._paid_at

    @paid_at.setter
    def paid_at(self, paid_at):
        """Sets the paid_at of this Package.

        The time when the pay was made. ISO_8601 format  # noqa: E501

        :param paid_at: The paid_at of this Package.  # noqa: E501
        :type: str
        """

        self._paid_at = paid_at

    @property
    def products_total_tax(self):
        """Gets the products_total_tax of this Package.  # noqa: E501

        The sum tax of all products in current order, including Non-cash deduction amount.  # noqa: E501

        :return: The products_total_tax of this Package.  # noqa: E501
        :rtype: float
        """
        return self._products_total_tax

    @products_total_tax.setter
    def products_total_tax(self, products_total_tax):
        """Sets the products_total_tax of this Package.

        The sum tax of all products in current order, including Non-cash deduction amount.  # noqa: E501

        :param products_total_tax: The products_total_tax of this Package.  # noqa: E501
        :type: float
        """

        self._products_total_tax = products_total_tax

    @property
    def shipping_cost(self):
        """Gets the shipping_cost of this Package.  # noqa: E501

        The shipping cost of current order, excluding the shipping cost on each contained products. If delivery free, just set 0.  # noqa: E501

        :return: The shipping_cost of this Package.  # noqa: E501
        :rtype: float
        """
        return self._shipping_cost

    @shipping_cost.setter
    def shipping_cost(self, shipping_cost):
        """Sets the shipping_cost of this Package.

        The shipping cost of current order, excluding the shipping cost on each contained products. If delivery free, just set 0.  # noqa: E501

        :param shipping_cost: The shipping_cost of this Package.  # noqa: E501
        :type: float
        """

        self._shipping_cost = shipping_cost

    @property
    def non_cash_deduction_amount(self):
        """Gets the non_cash_deduction_amount of this Package.  # noqa: E501

        Amount that deducted by non-cash, e.g. member points, virtual currency, voucher code, etc.  # noqa: E501

        :return: The non_cash_deduction_amount of this Package.  # noqa: E501
        :rtype: float
        """
        return self._non_cash_deduction_amount

    @non_cash_deduction_amount.setter
    def non_cash_deduction_amount(self, non_cash_deduction_amount):
        """Sets the non_cash_deduction_amount of this Package.

        Amount that deducted by non-cash, e.g. member points, virtual currency, voucher code, etc.  # noqa: E501

        :param non_cash_deduction_amount: The non_cash_deduction_amount of this Package.  # noqa: E501
        :type: float
        """

        self._non_cash_deduction_amount = non_cash_deduction_amount

    @property
    def customer_note(self):
        """Gets the customer_note of this Package.  # noqa: E501

        The special note from the buyer.  # noqa: E501

        :return: The customer_note of this Package.  # noqa: E501
        :rtype: str
        """
        return self._customer_note

    @customer_note.setter
    def customer_note(self, customer_note):
        """Sets the customer_note of this Package.

        The special note from the buyer.  # noqa: E501

        :param customer_note: The customer_note of this Package.  # noqa: E501
        :type: str
        """

        self._customer_note = customer_note

    @property
    def cancel_reason(self):
        """Gets the cancel_reason of this Package.  # noqa: E501

        The cancel reason of current package.  # noqa: E501

        :return: The cancel_reason of this Package.  # noqa: E501
        :rtype: str
        """
        return self._cancel_reason

    @cancel_reason.setter
    def cancel_reason(self, cancel_reason):
        """Sets the cancel_reason of this Package.

        The cancel reason of current package.  # noqa: E501

        :param cancel_reason: The cancel_reason of this Package.  # noqa: E501
        :type: str
        """

        self._cancel_reason = cancel_reason

    @property
    def warehouse_code(self):
        """Gets the warehouse_code of this Package.  # noqa: E501

        The code of warehouse for this package  # noqa: E501

        :return: The warehouse_code of this Package.  # noqa: E501
        :rtype: str
        """
        return self._warehouse_code

    @warehouse_code.setter
    def warehouse_code(self, warehouse_code):
        """Sets the warehouse_code of this Package.

        The code of warehouse for this package  # noqa: E501

        :param warehouse_code: The warehouse_code of this Package.  # noqa: E501
        :type: str
        """

        self._warehouse_code = warehouse_code

    @property
    def customer_id_ref(self):
        """Gets the customer_id_ref of this Package.  # noqa: E501

        The ID of buyer on current third party platform.  # noqa: E501

        :return: The customer_id_ref of this Package.  # noqa: E501
        :rtype: str
        """
        return self._customer_id_ref

    @customer_id_ref.setter
    def customer_id_ref(self, customer_id_ref):
        """Sets the customer_id_ref of this Package.

        The ID of buyer on current third party platform.  # noqa: E501

        :param customer_id_ref: The customer_id_ref of this Package.  # noqa: E501
        :type: str
        """

        self._customer_id_ref = customer_id_ref

    @property
    def insurance_fee(self):
        """Gets the insurance_fee of this Package.  # noqa: E501

        The insurance fee of current shipping.  # noqa: E501

        :return: The insurance_fee of this Package.  # noqa: E501
        :rtype: float
        """
        return self._insurance_fee

    @insurance_fee.setter
    def insurance_fee(self, insurance_fee):
        """Sets the insurance_fee of this Package.

        The insurance fee of current shipping.  # noqa: E501

        :param insurance_fee: The insurance_fee of this Package.  # noqa: E501
        :type: float
        """

        self._insurance_fee = insurance_fee

    @property
    def express_type(self):
        """Gets the express_type of this Package.  # noqa: E501


        :return: The express_type of this Package.  # noqa: E501
        :rtype: str
        """
        return self._express_type

    @express_type.setter
    def express_type(self, express_type):
        """Sets the express_type of this Package.


        :param express_type: The express_type of this Package.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and express_type is None:  # noqa: E501
            raise ValueError("Invalid value for `express_type`, must not be `None`")  # noqa: E501

        self._express_type = express_type

    @property
    def payment_pay_id(self):
        """Gets the payment_pay_id of this Package.  # noqa: E501

        The payment number generated by payment tool such as WeChat Pay  # noqa: E501

        :return: The payment_pay_id of this Package.  # noqa: E501
        :rtype: str
        """
        return self._payment_pay_id

    @payment_pay_id.setter
    def payment_pay_id(self, payment_pay_id):
        """Sets the payment_pay_id of this Package.

        The payment number generated by payment tool such as WeChat Pay  # noqa: E501

        :param payment_pay_id: The payment_pay_id of this Package.  # noqa: E501
        :type: str
        """

        self._payment_pay_id = payment_pay_id

    @property
    def platform_name(self):
        """Gets the platform_name of this Package.  # noqa: E501

        The e-commerce platform name, available options: youzan, pdd, nomad  # noqa: E501

        :return: The platform_name of this Package.  # noqa: E501
        :rtype: str
        """
        return self._platform_name

    @platform_name.setter
    def platform_name(self, platform_name):
        """Sets the platform_name of this Package.

        The e-commerce platform name, available options: youzan, pdd, nomad  # noqa: E501

        :param platform_name: The platform_name of this Package.  # noqa: E501
        :type: str
        """

        self._platform_name = platform_name

    @property
    def check_point(self):
        """Gets the check_point of this Package.  # noqa: E501

        log express check point, turn on it by input \"enable\", default is disabled  # noqa: E501

        :return: The check_point of this Package.  # noqa: E501
        :rtype: str
        """
        return self._check_point

    @check_point.setter
    def check_point(self, check_point):
        """Sets the check_point of this Package.

        log express check point, turn on it by input \"enable\", default is disabled  # noqa: E501

        :param check_point: The check_point of this Package.  # noqa: E501
        :type: str
        """

        self._check_point = check_point

    @property
    def items(self):
        """Gets the items of this Package.  # noqa: E501

        Contents of package  # noqa: E501

        :return: The items of this Package.  # noqa: E501
        :rtype: list[PackageItem]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this Package.

        Contents of package  # noqa: E501

        :param items: The items of this Package.  # noqa: E501
        :type: list[PackageItem]
        """

        self._items = items

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
        if not isinstance(other, Package):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Package):
            return True

        return self.to_dict() != other.to_dict()
