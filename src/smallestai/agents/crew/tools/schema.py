import inspect
import re
from typing import Any, Callable, Dict, List, Optional, get_args, get_origin, get_type_hints

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


def python_type_to_json_type(type_hint: Any) -> str:
    """
    Convert Python type hint to JSON schema type.

    Args:
        type_hint: Python type hint

    Returns:
        JSON schema type string
    """
    # Handle None/NoneType
    if type_hint is None or type_hint is type(None):
        return "null"

    origin = get_origin(type_hint)

    if origin in (list, List):
        return "array"

    # Handle Dict, dict
    if origin in (dict, Dict):
        return "object"

    # Handle basic types
    if type_hint == str:
        return "string"
    if type_hint in (int, float):
        return "number"
    if type_hint == bool:
        return "boolean"

    # Default to string
    return "string"


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

        if get_origin(type_hint).__name__ == "Annotated" if get_origin(type_hint) else False:
            args = get_args(type_hint)
            if args:
                base_type = args[0]
                for metadata in args[1:]:
                    if isinstance(metadata, FieldInfo) and metadata.description:
                        param_desc = metadata.description
                        break
                type_hint = base_type

        json_type = python_type_to_json_type(type_hint)
        properties[param_name] = {"type": json_type, "description": param_desc}

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
