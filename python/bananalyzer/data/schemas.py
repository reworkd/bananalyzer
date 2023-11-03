from abc import ABC, abstractmethod
from typing import Dict, Literal, Union, Any, List

from pydantic import BaseModel, Field

GoalType = Literal[
    "fetch",  # Scrape specific JSON information from a single page. Does not require navigation
    "navigate",  # Travel to a new page
    "search",  # Search for the answer to a specific query
    "multiple",  # Perform multiple intents
]


class Eval(BaseModel, ABC):
    """
    Base class for all evals. Evals are used to determine if an action or result is correct
    """

    @abstractmethod
    def eval_action(self, action: str) -> bool:
        raise NotImplementedError("eval_action not implemented")

    @abstractmethod
    def eval_result(self, result: str) -> bool:
        raise NotImplementedError("eval_result not implemented")


class JSONEval(BaseModel):
    type: Literal["json_match"] = Field(default="json_match")
    expected: Dict[str, Any]

    def eval_action(self, _: str) -> bool:
        # We don't care about action level evaluations
        return True

    def eval_results(self, result: Dict[str, Any]) -> bool:
        return result == self.expected


class ActionEval(BaseModel):
    actions: Dict[str, str]


class Example(BaseModel):
    id: str
    url: str
    source: Literal["mhtml", "hosted"] = Field(description="Source of the website")
    domain: str = Field(description="Domain of the website")
    subdomain: str = Field(description="Subdomain of the website")
    type: GoalType = Field(
        description="The high level type of goal the agent is aiming to do"
    )
    goal: Union[str, Dict[str, Any]] = Field(
        description="The goal of the agent for this specific example"
    )
    evals: List[Union[JSONEval]] = Field(
        "Various evaluations to test for within the example"
    )
