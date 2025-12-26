"""
BackgroundAgentNode - Base class for agents that do internal processing.

Features:
- Does NOT handle CONTROL_INTERRUPT
- No automatic output events
- Use for: sentiment analysis, data extraction, background reasoning
"""

from smallestai.atoms.agent.events import SDKEvent
from smallestai.atoms.agent.nodes.base import Node


class BackgroundAgentNode(Node):
    """
    Base class for agents that do internal processing without output.

    This node type:
    - Does NOT automatically handle CONTROL_INTERRUPT
    - Does NOT emit output events automatically
    - Is designed for background processing like sentiment analysis, data extraction, etc.
    - Stores results internally or sends custom events

    Usage:
        class SentimentAnalyzer(BackgroundAgentNode):
            def __init__(self):
                super().__init__(name="sentiment")
                self.llm = OpenAIClient(model="gpt-4o-mini")
                self.results = {}

            async def process_event(self, event):
                if event.type == EventType.USER_TRANSCRIPTION:
                    sentiment = await self.analyze(event.text)
                    self.results[event.timestamp] = sentiment
                    # No output events - stores internally

            async def analyze(self, text: str):
                response = await self.llm.chat(
                    messages=[
                        {"role": "system", "content": "Analyze sentiment"},
                        {"role": "user", "content": text}
                    ]
                )
                return response.content
    """

    async def process_event(self, event: SDKEvent):
        """
        Process events (override in subclass).

        Note: This node type does NOT automatically handle interrupts.
        Override this method to handle events specific to your use case.

        Args:
            event: Event to process
        """
        pass
