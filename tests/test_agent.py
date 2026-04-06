import pytest


class DummyAgent:
    async def run(self, user_prompt):
        class Response:
            output = "Test response"

            def new_messages(self):
                return []

        return Response()


@pytest.mark.asyncio
async def test_agent_run():
    agent = DummyAgent()
    result = await agent.run("test question")
    assert result.output == "Test response"
