from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from playwright.async_api import Page

from bananalyzer.data.schemas import Example

AgentResult = Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]


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
