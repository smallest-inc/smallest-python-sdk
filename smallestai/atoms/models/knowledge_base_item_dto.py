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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class KnowledgeBaseItemDTO(BaseModel):
    """
    KnowledgeBaseItemDTO
    """ # noqa: E501
    id: StrictStr = Field(alias="_id")
    item_type: Optional[StrictStr] = Field(default=None, alias="itemType")
    metadata: Optional[Dict[str, Any]] = None
    knowledge_base_id: Optional[StrictStr] = Field(default=None, alias="knowledgeBaseId")
    processing_status: Optional[StrictStr] = Field(default=None, alias="processingStatus")
    content_type: Optional[StrictStr] = Field(default=None, alias="contentType")
    size: Optional[Union[StrictFloat, StrictInt]] = None
    key: Optional[StrictStr] = None
    title: Optional[StrictStr] = None
    content: Optional[StrictStr] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")
    __properties: ClassVar[List[str]] = ["_id", "itemType", "metadata", "knowledgeBaseId", "processingStatus", "contentType", "size", "key", "title", "content", "createdAt", "updatedAt"]

    @field_validator('item_type')
    def item_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['file', 'text']):
            raise ValueError("must be one of enum values ('file', 'text')")
        return value

    @field_validator('processing_status')
    def processing_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['pending', 'processing', 'completed', 'failed']):
            raise ValueError("must be one of enum values ('pending', 'processing', 'completed', 'failed')")
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
        """Create an instance of KnowledgeBaseItemDTO from a JSON string"""
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
        """Create an instance of KnowledgeBaseItemDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "_id": obj.get("_id"),
            "itemType": obj.get("itemType"),
            "metadata": obj.get("metadata"),
            "knowledgeBaseId": obj.get("knowledgeBaseId"),
            "processingStatus": obj.get("processingStatus"),
            "contentType": obj.get("contentType"),
            "size": obj.get("size"),
            "key": obj.get("key"),
            "title": obj.get("title"),
            "content": obj.get("content"),
            "createdAt": obj.get("createdAt"),
            "updatedAt": obj.get("updatedAt")
        })
        return _obj


