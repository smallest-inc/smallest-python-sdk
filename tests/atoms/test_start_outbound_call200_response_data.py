# coding: utf-8

"""
    Agent Management API

    API for managing agents, their templates, and call logs

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from smallestai.atoms.models.start_outbound_call200_response_data import StartOutboundCall200ResponseData

class TestStartOutboundCall200ResponseData(unittest.TestCase):
    """StartOutboundCall200ResponseData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> StartOutboundCall200ResponseData:
        """Test StartOutboundCall200ResponseData
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `StartOutboundCall200ResponseData`
        """
        model = StartOutboundCall200ResponseData()
        if include_optional:
            return StartOutboundCall200ResponseData(
                call_id = 'abc123'
            )
        else:
            return StartOutboundCall200ResponseData(
        )
        """

    def testStartOutboundCall200ResponseData(self):
        """Test StartOutboundCall200ResponseData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
