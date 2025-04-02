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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from smallestai.atoms.models.create_agent_request_language_synthesizer_voice_config import CreateAgentRequestLanguageSynthesizerVoiceConfig
from typing import Optional, Set
from typing_extensions import Self

class CreateAgentRequestLanguageSynthesizer(BaseModel):
    """
    Synthesizer configuration for the agent. You can configure the synthesizer to use different voices and models. Currently we support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform https://waves.smallest.ai/voice-clone and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice. When updating the synthesizer configuration to voice clone model, you have to provide model and voiceId and gender all are required fields but when selecting the model as waves or waves and waves_lightning_large, you have to provide only model field and voiceId.
    """ # noqa: E501
    voice_config: Optional[CreateAgentRequestLanguageSynthesizerVoiceConfig] = Field(default=None, alias="voiceConfig")
    speed: Optional[Union[StrictFloat, StrictInt]] = 1.2
    consistency: Optional[Union[Annotated[float, Field(le=1, strict=True, ge=0)], Annotated[int, Field(le=1, strict=True, ge=0)]]] = 0.5
    similarity: Optional[Union[Annotated[float, Field(le=1, strict=True, ge=0)], Annotated[int, Field(le=1, strict=True, ge=0)]]] = 0
    enhancement: Optional[Union[StrictFloat, StrictInt]] = 1
    __properties: ClassVar[List[str]] = ["voiceConfig", "speed", "consistency", "similarity", "enhancement"]

    @field_validator('enhancement')
    def enhancement_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set([0, 1, 2]):
            raise ValueError("must be one of enum values (0, 1, 2)")
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
        """Create an instance of CreateAgentRequestLanguageSynthesizer from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of voice_config
        if self.voice_config:
            _dict['voiceConfig'] = self.voice_config.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateAgentRequestLanguageSynthesizer from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "voiceConfig": CreateAgentRequestLanguageSynthesizerVoiceConfig.from_dict(obj["voiceConfig"]) if obj.get("voiceConfig") is not None else None,
            "speed": obj.get("speed") if obj.get("speed") is not None else 1.2,
            "consistency": obj.get("consistency") if obj.get("consistency") is not None else 0.5,
            "similarity": obj.get("similarity") if obj.get("similarity") is not None else 0,
            "enhancement": obj.get("enhancement") if obj.get("enhancement") is not None else 1
        })
        return _obj


