# coding: utf-8

"""
    Agent Management API

    API for managing agents, their templates, and call logs

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from smallestai.atoms.models.get_knowledge_base_by_id200_response_data import GetKnowledgeBaseById200ResponseData

class TestGetKnowledgeBaseById200ResponseData(unittest.TestCase):
    """GetKnowledgeBaseById200ResponseData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetKnowledgeBaseById200ResponseData:
        """Test GetKnowledgeBaseById200ResponseData
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetKnowledgeBaseById200ResponseData`
        """
        model = GetKnowledgeBaseById200ResponseData()
        if include_optional:
            return GetKnowledgeBaseById200ResponseData(
                id = '',
                item_type = 'file',
                metadata = None,
                knowledge_base_id = '',
                processing_status = 'pending',
                content_type = '',
                size = 1.337,
                key = '',
                title = '',
                content = '',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return GetKnowledgeBaseById200ResponseData(
                id = '',
                item_type = 'file',
                knowledge_base_id = '',
                processing_status = 'pending',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
        )
        """

    def testGetKnowledgeBaseById200ResponseData(self):
        """Test GetKnowledgeBaseById200ResponseData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
