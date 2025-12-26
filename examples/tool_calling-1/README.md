# Tool Calling Example

This example demonstrates how to integrate tool calling with agents using the decorator pattern.

## Overview

The assistant agent can call tools to perform specific tasks:
- **get_weather**: Get weather information for a location
- **calculate**: Perform mathematical operations
- **get_current_time**: Get current time in any timezone

## Files

- `tools.py` - Tool definitions using `@function_tool` decorator
- `assistant_agent.py` - Agent that uses tools
- `server.py` - Server setup
- `client.py` - Test client

## How It Works

### 1. Define Tools with Decorator

```python
from sdk.tools import function_tool

@function_tool
async def get_weather(location: str, unit: str = "celsius"):
    """Get current weather for a location.

    Args:
        location: City and state
        unit: Temperature unit
    """
    # Implementation
    return {"temperature": 18, "conditions": "Foggy"}
```

### 2. Register Tools in Agent

```python
from sdk.tools import ToolRegistry

class AssistantAgent(OutputAgentNode):
    def __init__(self):
        super().__init__(name="assistant")
        self.llm = OpenAIClient(model="gpt-4o")

        # Create registry
        self.tool_registry = ToolRegistry()

        # Register tools
        self.tool_registry.register(get_weather)
        self.tool_registry.register(calculate)

        # Get schemas for LLM
        self.tool_schemas = self.tool_registry.get_schemas()
```

### 3. Use Tools in generate_response

```python
async def generate_response(self, messages):
    # Call LLM with tools
    response = await self.llm.chat(
        messages=messages,
        tools=self.tool_schemas
    )

    # Execute tool calls if requested
    if response.tool_calls:
        tool_results = await self.tool_registry.execute(
            response.tool_calls,
            parallel=True
        )

        # Add results to conversation and get final response
        # ... (see assistant_agent.py for full implementation)
```

## Running the Example

### Start Server

```bash
cd examples/tool_calling
python server.py
```

### Test with Client

In another terminal:

```bash
python client.py
```

## Example Interactions

**Weather Query**:
```
User: What's the weather in San Francisco?
Assistant: The current weather in San Francisco, CA is 18°C and foggy.
```

**Math Calculation**:
```
User: Calculate 15 multiply 7
Assistant: 15 × 7 = 105
```

**Time Query**:
```
User: What time is it in Tokyo?
Assistant: The current time in Tokyo (Asia/Tokyo timezone) is 2024-01-15 14:30:00.
```

## Key Concepts

### Tool Decorator

The `@function_tool` decorator:
- Automatically extracts schema from type hints
- Reads descriptions from docstrings
- Makes functions callable by LLMs

### Tool Registry

The `ToolRegistry`:
- Manages registered tools
- Generates OpenAI-compatible schemas
- Executes tool calls with parallel support

### Automatic Schema Generation

Schema is generated from:
```python
@function_tool
async def get_weather(location: str, unit: str = "celsius"):
    """Get current weather.

    Args:
        location: City and state  # Used in schema description
        unit: Temperature unit     # Used in schema description
    """
```

Becomes:
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather.",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {"type": "string", "description": "City and state"},
        "unit": {"type": "string", "description": "Temperature unit"}
      },
      "required": ["location"]
    }
  }
}
```

## Next Steps

- See [TOOL_CALLING.md](../../TOOL_CALLING.md) for comprehensive documentation
- Future example: Schema-based tool calling (without decorators)

## Dependencies

Requires `pytz` for timezone support:
```bash
pip install pytz
```
