# coding: utf-8

"""
    printnanny-api-client

    Official API client library for print-nanny.com  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Contact: leigh@print-nanny.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import printnanny_api_client
from printnanny_api_client.models.release_request import ReleaseRequest  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestReleaseRequest(unittest.TestCase):
    """ReleaseRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ReleaseRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.release_request.ReleaseRequest()  # noqa: E501
        if include_optional :
            return ReleaseRequest(
                ansible_extra_vars = printnanny_api_client.models.ansible_extra_vars_request.AnsibleExtraVarsRequest(
                    janus_version = '0', 
                    janus_libwebsockets_version = '0', 
                    janus_libnice_version = '0', 
                    janus_usrsctp_version = '0', 
                    janus_libsrtp_version = '0', 
                    tflite_version = '0', 
                    printnanny_cli_version = '0', 
                    libcamera_version = '0', ), 
                release_channel = 'stable'
            )
        else :
            return ReleaseRequest(
                ansible_extra_vars = printnanny_api_client.models.ansible_extra_vars_request.AnsibleExtraVarsRequest(
                    janus_version = '0', 
                    janus_libwebsockets_version = '0', 
                    janus_libnice_version = '0', 
                    janus_usrsctp_version = '0', 
                    janus_libsrtp_version = '0', 
                    tflite_version = '0', 
                    printnanny_cli_version = '0', 
                    libcamera_version = '0', ),
        )

    def testReleaseRequest(self):
        """Test ReleaseRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
