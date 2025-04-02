# coding: utf-8

"""
    Agent Management API

    API for managing agents, their templates, and call logs

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from smallestai.atoms.models.get_agents200_response_data import GetAgents200ResponseData

class TestGetAgents200ResponseData(unittest.TestCase):
    """GetAgents200ResponseData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetAgents200ResponseData:
        """Test GetAgents200ResponseData
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetAgents200ResponseData`
        """
        model = GetAgents200ResponseData()
        if include_optional:
            return GetAgents200ResponseData(
                agents = [
                    atoms_client.models.agent_dto.AgentDTO(
                        _id = '60d0fe4f5311236168a109ca', 
                        name = 'Customer Support Agent', 
                        description = 'This agent handles customer support inquiries and helps resolve common issues.', 
                        organization = '60d0fe4f5311236168a109cb', 
                        workflow_id = '60d0fe4f5311236168a109cc', 
                        created_by = '60d0fe4f5311236168a109cd', 
                        global_knowledge_base_id = '60d0fe4f5311236168a109ce', 
                        language = atoms_client.models.agent_dto_language.AgentDTO_language(
                            enabled = 'en', 
                            switching = False, 
                            supported = ["en","hi"], ), 
                        synthesizer = atoms_client.models.agent_dto_synthesizer.AgentDTO_synthesizer(
                            voice_config = atoms_client.models.agent_dto_synthesizer_voice_config.AgentDTO_synthesizer_voiceConfig(
                                model = 'waves_lightning_large', 
                                voice_id = 'nyah', 
                                gender = 'female', ), 
                            speed = 1.337, 
                            consistency = 0.5, 
                            similarity = 0, 
                            enhancement = 1, ), 
                        slm_model = 'atoms-slm-v1', 
                        default_variables = {"companyName":"Acme Corp","productName":"Widgets","supportEmail":"support@acmecorp.com"}, 
                        created_at = '2023-01-01T12:00Z', 
                        updated_at = '2023-01-02T14:30Z', )
                    ],
                total_count = 0,
                has_more = False,
                is_search_results = False
            )
        else:
            return GetAgents200ResponseData(
        )
        """

    def testGetAgents200ResponseData(self):
        """Test GetAgents200ResponseData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
