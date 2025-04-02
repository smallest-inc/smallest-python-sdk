# coding: utf-8

"""
    Agent Management API

    API for managing agents, their templates, and call logs

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from smallestai.atoms.models.start_outbound_call_request import StartOutboundCallRequest

class TestStartOutboundCallRequest(unittest.TestCase):
    """StartOutboundCallRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> StartOutboundCallRequest:
        """Test StartOutboundCallRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `StartOutboundCallRequest`
        """
        model = StartOutboundCallRequest()
        if include_optional:
            return StartOutboundCallRequest(
                agent_id = '60d0fe4f5311236168a109ca',
                phone_number = '+1234567890'
            )
        else:
            return StartOutboundCallRequest(
                agent_id = '60d0fe4f5311236168a109ca',
                phone_number = '+1234567890',
        )
        """

    def testStartOutboundCallRequest(self):
        """Test StartOutboundCallRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
