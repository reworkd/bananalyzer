from abc import ABC, abstractmethod
from typing import Any, Dict, List

from playwright.async_api import Page

from bananalyzer.data.schemas import Example

AgentResult = Dict[str, Any] | List[Dict[str, Any]] | List[str] | str | None


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
