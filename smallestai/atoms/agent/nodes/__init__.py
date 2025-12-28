"""
Specialized base node classes for different agent behaviors.
"""

from smallestai.atoms.agent.nodes.background_agent import BackgroundAgentNode
from smallestai.atoms.agent.nodes.base import Node
from smallestai.atoms.agent.nodes.output_agent import OutputAgentNode

__all__ = ["BackgroundAgentNode", "OutputAgentNode", "Node"]
