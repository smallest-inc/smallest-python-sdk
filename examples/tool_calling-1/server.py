"""Tool calling example server."""

from assistant_agent import AssistantAgent
from loguru import logger

from smallestai.atoms.agent.server import AtomsApp
from smallestai.atoms.agent.session import AgentSession


async def setup_tool_calling_session(session: AgentSession):
    """Configure assistant agent with tool calling."""
    assistant = AssistantAgent()
    session.add_node(assistant)
    await session.start()
    await assistant.speak("Hello, how can I help you today?")
    await session.wait_until_complete()
    logger.success("Session complete")


if __name__ == "__main__":
    app = AtomsApp(setup_handler=setup_tool_calling_session)
    app.run()
