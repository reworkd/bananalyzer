from abc import ABC, abstractmethod

from playwright.async_api import Page

from bananalyzer.data.schemas import Example
from bananalyzer.runner.evals import AllowedJSON

AgentResult = AllowedJSON


class AgentRunner(ABC):
    """
    Wrapper class clients must implement to run an agent against the evaluations
    """

    @abstractmethod
    async def run(
        self,
        page: Page,
        eval_context: Example,
    ) -> AgentResult:
        pass
