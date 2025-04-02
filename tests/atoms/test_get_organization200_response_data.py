# coding: utf-8

"""
    Agent Management API

    API for managing agents, their templates, and call logs

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from smallestai.atoms.models.get_organization200_response_data import GetOrganization200ResponseData

class TestGetOrganization200ResponseData(unittest.TestCase):
    """GetOrganization200ResponseData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetOrganization200ResponseData:
        """Test GetOrganization200ResponseData
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetOrganization200ResponseData`
        """
        model = GetOrganization200ResponseData()
        if include_optional:
            return GetOrganization200ResponseData(
                id = '',
                name = '',
                members = [
                    atoms_client.models.get_organization_200_response_data_members_inner.getOrganization_200_response_data_members_inner(
                        _id = '', 
                        user_email = '', )
                    ],
                subscription = atoms_client.models.get_organization_200_response_data_subscription.getOrganization_200_response_data_subscription(
                    plan_id = '', )
            )
        else:
            return GetOrganization200ResponseData(
        )
        """

    def testGetOrganization200ResponseData(self):
        """Test GetOrganization200ResponseData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
