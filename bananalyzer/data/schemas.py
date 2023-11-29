from typing import Any, Dict, List, Literal, Optional, Union

from playwright.async_api import Page
from pydantic import BaseModel, Field, model_validator

from bananalyzer.data.fetch_schemas import get_fetch_schema
from bananalyzer.runner.evals import (
    validate_end_url_match,
    validate_field_match,
    validate_json_match,
)

GoalType = Literal[
    "fetch",  # Scrape specific JSON information from a single page. Does not require navigation
    "links",  # Scrape all detail page links from a single listing page
    "click",  # Make a single click on a page
    "navigate",  # Travel to a new page
    "search",  # Search for the answer to a specific query
    "multiple",  # Perform multiple intents
]


class Eval(BaseModel):
    """
    Base class for all evals. Evals are used to determine if an action or result is correct
    """

    type: Literal["json_match", "end_url_match"] = "json_match"
    expected: Union[Dict[str, Any], List[str], str]

    def eval_action(self, action: str) -> bool:
        """
        We don't care for action level evals at the moment
        """
        raise NotImplementedError("eval_action not implemented")

    def eval_results(
        self, page: Page, result: Dict[str, Any], field: Optional[str] = None
    ) -> None:
        if (
            self.type == "json_match"
            and field is not None
            and type(self.expected) is dict
        ):
            return validate_field_match(self.expected, result, field)

        if self.type == "json_match" and type(self.expected) is dict:
            return validate_json_match(self.expected, result)

        if self.type == "end_url_match" and type(self.expected) is str:
            return validate_end_url_match(self.expected, page.url)

        raise NotImplementedError("No evaluation type implemented")


class Example(BaseModel):
    id: str
    url: str
    source: Literal["mhtml", "hosted", "url"] = Field(
        description="Source of the website"
    )
    domain: str = Field(description="Domain of the website")
    subdomain: str = Field(description="Subdomain of the website")
    type: GoalType = Field(
        description="The high level goal intent the agent is aiming to do"
    )
    goal: Union[str, Dict[str, Any]] = Field(
        description="The goal of the agent for this specific example"
    )
    fetch_id: Optional[
        Literal["job_posting", "manufacturing_commerce", "contact", "forum"]
    ] = Field(
        default=None,
        description="If it is a fetch type, we can infer the goal based on this id to avoid large schemas in json",
    )
    evals: List[Eval] = Field(
        description="Various evaluations to test for within the example"
    )

    def get_static_url(self) -> str:
        from bananalyzer.runner.website_responder import get_website_responder

        return get_website_responder(self).get_url(self)

    @model_validator(mode="before")
    def set_goal_if_fetch_id_provided(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        goal_type = values.get("type")
        if goal_type != "fetch":
            return values

        fetch_id = values.get("fetch_id")
        if fetch_id is None:
            raise ValueError("fetch_id must be provided for fetch goal types")

        goal = values.get("goal")
        if goal is not None:
            raise ValueError("goal must not be provided if fetch_id is provided")

        values["goal"] = get_fetch_schema(fetch_id).model_fields
        return values
