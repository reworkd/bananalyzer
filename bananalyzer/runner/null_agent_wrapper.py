import asyncio

from playwright.async_api import Page

from bananalyzer.data.schemas import Example
from bananalyzer.runner.agent_runner import AgentResult, AgentRunner


class NullAgentRunner(AgentRunner):
    """
    A test agent class that just returns an empty string
    """

    RANDOM_FAILURE_RATE = 0  # You can change this to 0.5 to see random failures

    async def run(
        self,
        page: Page,
        example: Example,
    ) -> AgentResult:
        print(f"Testing {example.get_static_url()}")
        await page.goto(example.get_static_url())
        await asyncio.sleep(0.2)

        print(f"Done testing {example.get_static_url()}")

        # Ensure page is correct
        if example.evals[0].type == "end_url_match" and isinstance(
            example.evals[0].expected, str
        ):
            await page.goto(example.evals[0].expected)
            return example.evals[0].expected

        if example.evals[0].expected is not None:
            return example.evals[0].expected
        else:
            return example.evals[0].options[0]
