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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class UpdateAgentRequestLanguage(BaseModel):
    """
    Language configuration for the agent. You can enable or disable language switching for the agent. This will be used to determine the language of the agent.
    """ # noqa: E501
    enabled: Optional[StrictStr] = Field(default=None, description="The language of the agent. You can choose from the list of supported languages.")
    switching: Optional[StrictBool] = Field(default=False, description="Whether to enable language switching for the agent. If enabled, the agent will be able to switch between languages based on the user's language.")
    __properties: ClassVar[List[str]] = ["enabled", "switching"]

    @field_validator('enabled')
    def enabled_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['en', 'hi']):
            raise ValueError("must be one of enum values ('en', 'hi')")
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
        """Create an instance of UpdateAgentRequestLanguage from a JSON string"""
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
        """Create an instance of UpdateAgentRequestLanguage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "enabled": obj.get("enabled"),
            "switching": obj.get("switching") if obj.get("switching") is not None else False
        })
        return _obj


