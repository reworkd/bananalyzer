from playwright.async_api import BrowserContext

from bananalyzer.data.schemas import Example
from bananalyzer.runner.agent_runner import AgentResult, AgentRunner


class NullAgentRunner(AgentRunner):
    """
    A test agent class that just returns an empty string
    """

    async def run(
        self,
        context: BrowserContext,
        example: Example,
    ) -> AgentResult:
        page = await context.new_page()
        await page.goto(example.url)
        return example.evals[0].expected
