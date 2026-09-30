from .conftest import get_client, verify_request_count

from smallestai.atoms import RegistryToolDefinition


def test_atoms_tools_list_tools() -> None:
    """Test list_tools endpoint with WireMock"""
    test_id = "atoms.tools.list_tools.0"
    client = get_client(test_id)
    client.atoms.tools.list_tools()
    verify_request_count(test_id, "GET", "/tool", None, 1)


def test_atoms_tools_create_tool() -> None:
    """Test create_tool endpoint with WireMock"""
    test_id = "atoms.tools.create_tool.0"
    client = get_client(test_id)
    client.atoms.tools.create_tool(
        definition=RegistryToolDefinition(
            type="api_call",
            name="get_order_status",
            description="Look up a customer's order by id and read back its status.",
        ),
    )
    verify_request_count(test_id, "POST", "/tool", None, 1)


def test_atoms_tools_delete_tool() -> None:
    """Test delete_tool endpoint with WireMock"""
    test_id = "atoms.tools.delete_tool.0"
    client = get_client(test_id)
    client.atoms.tools.delete_tool(
        tool_id="toolId",
    )
    verify_request_count(test_id, "DELETE", "/tool/toolId", None, 1)


def test_atoms_tools_update_tool() -> None:
    """Test update_tool endpoint with WireMock"""
    test_id = "atoms.tools.update_tool.0"
    client = get_client(test_id)
    client.atoms.tools.update_tool(
        tool_id="toolId",
        definition=RegistryToolDefinition(
            type="api_call",
            name="get_order_status",
            description="Look up a customer's order by id and read back its status.",
        ),
    )
    verify_request_count(test_id, "PATCH", "/tool/toolId", None, 1)


def test_atoms_tools_duplicate_tool() -> None:
    """Test duplicate_tool endpoint with WireMock"""
    test_id = "atoms.tools.duplicate_tool.0"
    client = get_client(test_id)
    client.atoms.tools.duplicate_tool(
        tool_id="toolId",
    )
    verify_request_count(test_id, "POST", "/tool/toolId/duplicate", None, 1)
