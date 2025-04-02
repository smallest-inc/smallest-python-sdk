# coding: utf-8

"""
    Agent Management API

    API for managing agents, their templates, and call logs

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from smallestai.atoms.models.agent_dto_synthesizer import AgentDTOSynthesizer

class TestAgentDTOSynthesizer(unittest.TestCase):
    """AgentDTOSynthesizer unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AgentDTOSynthesizer:
        """Test AgentDTOSynthesizer
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AgentDTOSynthesizer`
        """
        model = AgentDTOSynthesizer()
        if include_optional:
            return AgentDTOSynthesizer(
                voice_config = atoms_client.models.agent_dto_synthesizer_voice_config.AgentDTO_synthesizer_voiceConfig(
                    model = 'waves_lightning_large', 
                    voice_id = 'nyah', 
                    gender = 'female', ),
                speed = 1.337,
                consistency = 0.5,
                similarity = 0,
                enhancement = 1
            )
        else:
            return AgentDTOSynthesizer(
        )
        """

    def testAgentDTOSynthesizer(self):
        """Test AgentDTOSynthesizer"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
