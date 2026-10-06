import enum
import inspect
import re
import sys
import types
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class FunctionSchema(BaseModel):
    """Schema for a function tool."""

    name: str
    description: str
    parameters: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI function format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


_UNION_TYPES: Tuple[Any, ...] = (Union,)
if sys.version_info >= (3, 10):
    _UNION_TYPES += (types.UnionType,)

_PRIMITIVES: Dict[Any, str] = {str: "string", bool: "boolean", int: "integer", float: "number"}


def python_type_to_json_schema(type_hint: Any) -> Dict[str, Any]:
    """
    Convert a Python type hint to a JSON schema fragment.

    Handles primitives, list/tuple/set (with ``items``), dict, Optional/Union,
    Literal and Enum. Unknown types fall back to ``{"type": "string"}``.

    Args:
        type_hint: Python type hint

    Returns:
        JSON schema dict
    """
    if type_hint is None or type_hint is type(None):
        return {"type": "null"}

    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Annotated[...] — detect via __metadata__ (stable across 3.9–3.12; get_origin(...)
    # is Annotated is not reliable on 3.9). Unwrap to the underlying type.
    if hasattr(type_hint, "__metadata__"):
        return python_type_to_json_schema(args[0])

    if origin in _UNION_TYPES:
        non_null = [a for a in args if a is not type(None)]
        if len(non_null) == 1:
            # Optional[X]: whether the argument may be omitted is expressed by
            # "required", so advertise X itself.
            return python_type_to_json_schema(non_null[0])
        return {"anyOf": [python_type_to_json_schema(a) for a in non_null]}

    if origin is Literal:
        schema: Dict[str, Any] = {"enum": list(args)}
        literal_types = {type(a) for a in args}
        if len(literal_types) == 1 and literal_types.pop() in _PRIMITIVES:
            schema["type"] = _PRIMITIVES[type(args[0])]
        return schema

    if type_hint in (list, tuple, set, frozenset) or origin in (list, tuple, set, frozenset):
        schema = {"type": "array"}
        # Array schemas must declare "items" (OpenAI rejects them otherwise).
        item_args = [a for a in args if a is not Ellipsis]
        if len(set(item_args)) == 1:
            schema["items"] = python_type_to_json_schema(item_args[0])
        elif item_args:
            schema["items"] = {"anyOf": [python_type_to_json_schema(a) for a in item_args]}
        else:
            schema["items"] = {}
        return schema

    if type_hint is dict or origin is dict:
        return {"type": "object"}

    if inspect.isclass(type_hint) and issubclass(type_hint, enum.Enum):
        values = [member.value for member in type_hint]
        schema = {"enum": values}
        value_types = {type(v) for v in values}
        if len(value_types) == 1 and next(iter(value_types)) in _PRIMITIVES:
            schema["type"] = _PRIMITIVES[type(values[0])]
        return schema

    if type_hint in _PRIMITIVES:
        return {"type": _PRIMITIVES[type_hint]}

    # Default to string
    return {"type": "string"}


def python_type_to_json_type(type_hint: Any) -> str:
    """
    Convert Python type hint to JSON schema type.

    Kept for backward compatibility; prefer ``python_type_to_json_schema``,
    which also carries ``items``/``enum``/``anyOf``.

    Args:
        type_hint: Python type hint

    Returns:
        JSON schema type string
    """
    return python_type_to_json_schema(type_hint).get("type", "string")


def parse_docstring(docstring: str) -> Dict[str, Any]:
    """
    Parse Google-style docstring to extract description and parameters.

    Args:
        docstring: Function docstring

    Returns:
        Dict with 'description' and 'params' (dict of param names to descriptions)
    """
    if not docstring:
        return {"description": "", "params": {}}

    lines = docstring.strip().split("\n")

    description_lines = []
    params = {}

    in_args_section = False
    current_param = None
    current_param_desc = []

    for line in lines:
        stripped = line.strip()

        if stripped in ("Args:", "Arguments:", "Parameters:"):
            in_args_section = True
            continue

        if not in_args_section:
            if stripped:
                description_lines.append(stripped)
        else:
            match = re.match(r"^(\w+)(\s*\([^)]+\))?\s*:\s*(.+)$", stripped)
            if match:
                if current_param:
                    params[current_param] = " ".join(current_param_desc)

                current_param = match.group(1)
                current_param_desc = [match.group(3)]
            elif current_param and stripped:
                current_param_desc.append(stripped)

    # Save last param
    if current_param:
        params[current_param] = " ".join(current_param_desc)

    description = " ".join(description_lines)

    return {"description": description, "params": params}


def extract_function_schema(
    func: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> FunctionSchema:
    """
    Extract JSON schema from function signature and docstring.

    Args:
        func: Function to extract schema from
        name: Override function name
        description: Override description

    Returns:
        FunctionSchema with extracted metadata

    Example:
        def get_weather(location: str, format: str = "celsius"):
            '''Get current weather.

            Args:
                location: City and state
                format: Temperature format
            '''
            pass

        schema = extract_function_schema(get_weather)
        # schema.name == "get_weather"
        # schema.parameters["properties"]["location"]["type"] == "string"
    """
    signature = inspect.signature(func)
    type_hints = get_type_hints(func, include_extras=True)

    docstring_info = parse_docstring(func.__doc__ or "")

    properties: Dict[str, Any] = {}
    required: List[str] = []

    for param_name, param in signature.parameters.items():
        if param_name in ("self", "cls"):
            continue

        type_hint = type_hints.get(param_name, Any)
        param_desc = docstring_info["params"].get(param_name, "")

        # Pull a FieldInfo description from Annotated metadata via the RAW annotation.
        # get_type_hints can bury the Annotated under an outer Optional when the param
        # has a None default (Python 3.9: Annotated[Optional[str], ...] = None resolves
        # to Optional[Annotated[...]]), hiding __metadata__; the raw annotation keeps it.
        # The resolved type_hint still renders the type correctly (it unwraps Optional +
        # Annotated), so we only mine the raw annotation for the description here.
        raw_annotation = param.annotation
        if hasattr(raw_annotation, "__metadata__"):
            for metadata in get_args(raw_annotation)[1:]:
                if isinstance(metadata, FieldInfo) and metadata.description:
                    param_desc = metadata.description
                    break

        properties[param_name] = {**python_type_to_json_schema(type_hint), "description": param_desc}

        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    return FunctionSchema(
        name=name or func.__name__,
        description=description or docstring_info["description"],
        parameters={
            "type": "object",
            "properties": properties,
            "required": required,
        },
    )
