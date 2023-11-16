import asyncio

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
        print(f"Testing {example.get_static_url()}")
        await page.goto(example.get_static_url())
        await asyncio.sleep(0.5)
        print(f"Done testing {example.get_static_url()}")
        return example.evals[0].expected  # type: ignore
