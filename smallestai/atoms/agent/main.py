from smallestai.atoms.agent.server import AtomsApp
from smallestai.atoms.agent.session import AgentSession

# class Agent(OpenAILLMNode):
#     def __init__(self, name: str):
#         super().__init__(
#             name=name,
#         )


async def run_agent(agent_session: AgentSession):
    """Default main - starts a simple echo server"""
    # agent = Agent(name="Agent")
    # agent_session.add_node(agent)
    # await agent_session.start()
    pass


app = AtomsApp(run_agent)
if __name__ == "__main__":
    app.run()
