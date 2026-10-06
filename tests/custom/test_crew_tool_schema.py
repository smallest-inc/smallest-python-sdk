"""Tool JSON schemas generated from type hints must describe what the tool
actually accepts: the registry passes LLM arguments through uncoerced, so a
wrong "type" reaches the tool function as a wrong Python type, and an array
without "items" is rejected outright by OpenAI."""

import enum
from typing import Annotated, Dict, List, Literal, Optional, Set, Tuple, Union

from pydantic import Field

from smallestai.atoms.crew.tools import function_tool
from smallestai.atoms.crew.tools.schema import (
    extract_function_schema,
    python_type_to_json_schema,
    python_type_to_json_type,
)


class Color(enum.Enum):
    RED = "red"
    BLUE = "blue"


def _props(func):
    return extract_function_schema(func).parameters["properties"]


def test_primitives():
    assert python_type_to_json_schema(str) == {"type": "string"}
    assert python_type_to_json_schema(int) == {"type": "integer"}
    assert python_type_to_json_schema(float) == {"type": "number"}
    assert python_type_to_json_schema(bool) == {"type": "boolean"}


def test_arrays_always_declare_items():
    assert python_type_to_json_schema(List[str]) == {"type": "array", "items": {"type": "string"}}
    assert python_type_to_json_schema(list) == {"type": "array", "items": {}}
    assert python_type_to_json_schema(Set[int]) == {"type": "array", "items": {"type": "integer"}}
    assert python_type_to_json_schema(Tuple[int, ...]) == {"type": "array", "items": {"type": "integer"}}
    assert python_type_to_json_schema(List[List[int]]) == {
        "type": "array",
        "items": {"type": "array", "items": {"type": "integer"}},
    }


def test_bare_and_parameterized_dict_are_objects():
    assert python_type_to_json_schema(dict) == {"type": "object"}
    assert python_type_to_json_schema(Dict[str, int]) == {"type": "object"}


def test_optional_advertises_inner_type():
    assert python_type_to_json_schema(Optional[int]) == {"type": "integer"}
    assert python_type_to_json_schema(Optional[List[str]]) == {"type": "array", "items": {"type": "string"}}


def test_multi_type_union_uses_anyof():
    assert python_type_to_json_schema(Union[int, str]) == {"anyOf": [{"type": "integer"}, {"type": "string"}]}


def test_literal_and_enum_carry_allowed_values():
    assert python_type_to_json_schema(Literal["std", "deluxe"]) == {"enum": ["std", "deluxe"], "type": "string"}
    assert python_type_to_json_schema(Color) == {"enum": ["red", "blue"], "type": "string"}


def test_unknown_types_still_default_to_string():
    class Custom:
        pass

    assert python_type_to_json_schema(Custom) == {"type": "string"}


def test_legacy_type_helper_still_returns_a_string():
    assert python_type_to_json_type(List[str]) == "array"
    assert python_type_to_json_type(Optional[int]) == "integer"
    assert python_type_to_json_type(Literal["a"]) == "string"


def test_function_tool_schema_end_to_end():
    @function_tool
    def book_room(
        guests: int,
        dates: List[str],
        room: Optional[int],
        kind: Literal["std", "deluxe"],
        note: Annotated[Optional[str], Field(description="Free text")] = None,
    ):
        """Book a room.

        Args:
            guests: Number of guests
            dates: ISO dates
        """

    params = book_room.__tool_info__.schema.parameters
    assert params["required"] == ["guests", "dates", "room", "kind"]
    assert params["properties"] == {
        "guests": {"type": "integer", "description": "Number of guests"},
        "dates": {"type": "array", "items": {"type": "string"}, "description": "ISO dates"},
        "room": {"type": "integer", "description": ""},
        "kind": {"enum": ["std", "deluxe"], "type": "string", "description": ""},
        "note": {"type": "string", "description": "Free text"},
    }


def test_existing_simple_signature_is_unchanged():
    def get_weather(location: str, format: str = "celsius"):
        """Get current weather.

        Args:
            location: City and state
            format: Temperature format
        """

    assert _props(get_weather) == {
        "location": {"type": "string", "description": "City and state"},
        "format": {"type": "string", "description": "Temperature format"},
    }


def test_special_form_params_do_not_crash():
    """Literal / Any params must not trip the Annotated check — ``get_origin`` returns a
    ``_SpecialForm`` for them, which has no ``__name__`` on Python 3.9 and used to crash."""
    from typing import Any

    from smallestai.atoms.crew.tools.schema import extract_function_schema

    def pick(mode: Literal["fast", "slow"], payload: Any):
        pass

    props = extract_function_schema(pick).parameters["properties"]
    assert props["mode"]["enum"] == ["fast", "slow"]
    assert props["mode"]["type"] == "string"
    assert props["payload"]["type"] == "string"  # Any -> string fallback
