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

import nomad_pilot_cli
from nomad_pilot_cli.api.callback_api import CallbackApi  # noqa: E501
from nomad_pilot_cli.rest import ApiException


class TestCallbackApi(unittest.TestCase):
    """CallbackApi unit test stubs"""

    def setUp(self):
        self.api = nomad_pilot_cli.api.callback_api.CallbackApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_callback(self):
        """Test case for callback

        callback  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
