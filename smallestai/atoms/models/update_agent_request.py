# coding: utf-8

"""
    Agent Management API

    API for managing agents, their templates, and call logs

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from smallestai.atoms.models.update_agent_request_language import UpdateAgentRequestLanguage
from smallestai.atoms.models.update_agent_request_synthesizer import UpdateAgentRequestSynthesizer
from typing import Optional, Set
from typing_extensions import Self

class UpdateAgentRequest(BaseModel):
    """
    UpdateAgentRequest
    """ # noqa: E501
    name: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    language: Optional[UpdateAgentRequestLanguage] = None
    synthesizer: Optional[UpdateAgentRequestSynthesizer] = None
    global_knowledge_base_id: Optional[StrictStr] = Field(default=None, alias="globalKnowledgeBaseId")
    slm_model: Optional[StrictStr] = Field(default='atoms-slm-v1', alias="slmModel")
    default_variables: Optional[Dict[str, Any]] = Field(default=None, description="The default variables to use for the agent. These variables will be used if no variables are provided when initiating a conversation with the agent.", alias="defaultVariables")
    telephony_product_id: Optional[StrictStr] = Field(default=None, description="The telephony product ID of the agent. This is the product ID of the telephony product that will be used to make the outbound call. You can buy telephone number and assign it to the agent.", alias="telephonyProductId")
    __properties: ClassVar[List[str]] = ["name", "description", "language", "synthesizer", "globalKnowledgeBaseId", "slmModel", "defaultVariables", "telephonyProductId"]

    @field_validator('slm_model')
    def slm_model_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['atoms-slm-v1', 'gpt-4o-mini']):
            raise ValueError("must be one of enum values ('atoms-slm-v1', 'gpt-4o-mini')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UpdateAgentRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of language
        if self.language:
            _dict['language'] = self.language.to_dict()
        # override the default output from pydantic by calling `to_dict()` of synthesizer
        if self.synthesizer:
            _dict['synthesizer'] = self.synthesizer.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdateAgentRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "language": UpdateAgentRequestLanguage.from_dict(obj["language"]) if obj.get("language") is not None else None,
            "synthesizer": UpdateAgentRequestSynthesizer.from_dict(obj["synthesizer"]) if obj.get("synthesizer") is not None else None,
            "globalKnowledgeBaseId": obj.get("globalKnowledgeBaseId"),
            "slmModel": obj.get("slmModel") if obj.get("slmModel") is not None else 'atoms-slm-v1',
            "defaultVariables": obj.get("defaultVariables"),
            "telephonyProductId": obj.get("telephonyProductId")
        })
        return _obj


