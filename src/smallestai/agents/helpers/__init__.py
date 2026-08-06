"""Utility classes for Atoms API operations."""

from smallestai.agents.helpers._envelope import Page, as_page, require_id
from smallestai.agents.helpers.agent_tools import AgentTools, AgentToolsError
from smallestai.agents.helpers.audience import Audience
from smallestai.agents.helpers.call import Call, CallAnalytics
from smallestai.agents.helpers.campaign import Campaign
from smallestai.agents.helpers.kb import KB
from smallestai.agents.helpers.versioning import (
    BaseRevisionUnavailableError,
    DraftConflictError,
    MigrationRequiredError,
    SecurityCheckFailedError,
    Versioning,
    VersioningError,
)

# Re-export the tool-config models so callers don't need their deep module paths
# (they are not exported from smallestai.agents.types).
from smallestai.agents.types.single_prompt_config import SinglePromptConfig
from smallestai.agents.types.tool import Tool
from smallestai.agents.types.tool_transfer_option import ToolTransferOption

__all__ = [
    "AgentTools",
    "AgentToolsError",
    "Audience",
    "CallAnalytics",
    "Call",
    "Campaign",
    "KB",
    "Page",
    "as_page",
    "require_id",
    "Versioning",
    "VersioningError",
    "MigrationRequiredError",
    "DraftConflictError",
    "BaseRevisionUnavailableError",
    "SecurityCheckFailedError",
    "SinglePromptConfig",
    "Tool",
    "ToolTransferOption",
]
