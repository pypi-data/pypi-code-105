# coding: utf-8

"""
    Nomad Pilot

    This is the API descriptor for the Nomad Pilot API, responsible for shipping and logistics processing. Developed by [Samarkand Global](https://www.samarkand.global/) in partnership with [SF Express](https://www.sf-express.com/), [eSinotrans](http://air.esinotrans.com/), [sto](http://sto-express.co.uk/). Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_pilot_cli` - Install for python with `pip install nomad-pilot-cli` - Install for Maven users `groupId, com.gitlab.samarkand-nomad; artifactId, nomad-pilot-cli`  # noqa: E501

    The version of the OpenAPI document: 1.44.21
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import nomad_pilot_cli
from nomad_pilot_cli.models.haiku_delivery_order import HaikuDeliveryOrder  # noqa: E501
from nomad_pilot_cli.rest import ApiException

class TestHaikuDeliveryOrder(unittest.TestCase):
    """HaikuDeliveryOrder unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test HaikuDeliveryOrder
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = nomad_pilot_cli.models.haiku_delivery_order.HaikuDeliveryOrder()  # noqa: E501
        if include_optional :
            return HaikuDeliveryOrder(
                delivery_order_code = '0', 
                delivery_order_id = '0', 
                warehouse_code = '0', 
                order_type = '0', 
                status = '0', 
                out_biz_code = '0', 
                confirm_type = '0', 
                order_confirm_time = '0', 
                operator_code = '0', 
                operator_name = '0', 
                operate_time = '0', 
                storage_fee = '0', 
                logistics_code = '0', 
                logistics_name = '0', 
                express_code = '0'
            )
        else :
            return HaikuDeliveryOrder(
        )

    def testHaikuDeliveryOrder(self):
        """Test HaikuDeliveryOrder"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
