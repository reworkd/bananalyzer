from playwright.async_api import BrowserContext

from bananalyzer.data.schemas import Example
from bananalyzer.runner.agent_wrapper import AgentResult, AgentWrapper


class NullAgentWrapper(AgentWrapper):
    """
    A test agent class that just returns an empty string
    """

    def run(
        self,
        _: BrowserContext,
        __: Example,
    ) -> AgentResult:
        return ""
