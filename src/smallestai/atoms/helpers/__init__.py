"""Utility classes for Atoms API operations."""

from smallestai.atoms.helpers.agent_tools import AgentTools, AgentToolsError
from smallestai.atoms.helpers.audience import Audience
from smallestai.atoms.helpers.call import Call, CallAnalytics
from smallestai.atoms.helpers.campaign import Campaign
from smallestai.atoms.helpers.kb import KB
from smallestai.atoms.helpers._envelope import Page, as_page, require_id
from smallestai.atoms.helpers.versioning import (
    Versioning,
    VersioningError,
    MigrationRequiredError,
    DraftConflictError,
    BaseRevisionUnavailableError,
    SecurityCheckFailedError,
)

# Re-export the tool-config models so callers don't need their deep module paths
# (they are not exported from smallestai.atoms.types).
from smallestai.atoms.types.single_prompt_config import SinglePromptConfig
from smallestai.atoms.types.tool import Tool
from smallestai.atoms.types.tool_transfer_option import ToolTransferOption

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
