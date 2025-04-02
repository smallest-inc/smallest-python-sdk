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
from typing import Optional, Set
from typing_extensions import Self

class UpdateAgentRequestSynthesizerVoiceConfigOneOf(BaseModel):
    """
    UpdateAgentRequestSynthesizerVoiceConfigOneOf
    """ # noqa: E501
    model: Optional[StrictStr] = Field(default=None, description="We currently support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice.")
    voice_id: Optional[StrictStr] = Field(default=None, alias="voiceId")
    gender: Optional[StrictStr] = Field(default=None, description="The gender of the synthesizer. When selecting gender, you have to select the model and voiceId which are required fields.")
    __properties: ClassVar[List[str]] = ["model", "voiceId", "gender"]

    @field_validator('model')
    def model_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['waves_lightning_large_voice_clone']):
            raise ValueError("must be one of enum values ('waves_lightning_large_voice_clone')")
        return value

    @field_validator('gender')
    def gender_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['male', 'female']):
            raise ValueError("must be one of enum values ('male', 'female')")
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
        """Create an instance of UpdateAgentRequestSynthesizerVoiceConfigOneOf from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdateAgentRequestSynthesizerVoiceConfigOneOf from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "model": obj.get("model"),
            "voiceId": obj.get("voiceId"),
            "gender": obj.get("gender")
        })
        return _obj


