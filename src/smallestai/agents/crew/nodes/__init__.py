"""
Specialized base node classes for different agent behaviors.
"""

from smallestai.agents.crew.nodes.background_crew import BackgroundCrewNode
from smallestai.agents.crew.nodes.base import CrewNode
from smallestai.agents.crew.nodes.output_crew import OutputCrewNode

__all__ = ["BackgroundCrewNode", "OutputCrewNode", "CrewNode"]
