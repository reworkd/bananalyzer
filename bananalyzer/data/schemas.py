from typing import Any, Dict, List, Literal, Optional, Union

from playwright.async_api import Page
from pydantic import BaseModel, Field, model_validator

from bananalyzer.runner.evals import (
    AllowedJSON,
    validate_end_url_match,
    validate_field_match,
    validate_json_match,
)

GoalType = Literal[
    "fetch",  # Scrape specific JSON information from a single page. Does not require navigation
    "links",  # Scrape all detail page links from a single listing page
    "links_fetch",  # Scrape all detail page links from a single listing page along with JSON information
    "pagination",  # Must fetch data across pages. Either links or fetch for now.
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
    expected: AllowedJSON

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
            and isinstance(self.expected, dict)
        ):
            return validate_field_match(self.expected, result, field)

        if self.type == "json_match" and isinstance(self.expected, (list, dict)):
            return validate_json_match(self.expected, result)

        if self.type == "end_url_match" and isinstance(self.expected, str):
            return validate_end_url_match(self.expected, page.url)

        raise NotImplementedError("No evaluation type implemented")


FetchId = Literal[
    "job_posting",
    "manufacturing_commerce",
    "contact",
    "forum",
    "attorney",
    "attorney_job_listing",
]


class Example(BaseModel):
    id: str
    url: str
    mhtml_url: Optional[str] = Field(
        description="URL of the mhtml file if it is hosted on e.g. AWS S3",
        default=None,
    )
    source: Literal["mhtml", "hosted"] = Field(description="Source of the website")
    category: str = Field(description="Category of the website")
    subcategory: str = Field(description="Subcategory of the website")
    type: GoalType = Field(
        description="The high level goal intent the agent is aiming to do"
    )
    goal: Optional[Union[str, Dict[str, Any]]] = Field(
        description="The goal of the agent for this specific example",
        default=None,
    )
    fetch_id: Optional[FetchId] = Field(
        description="If it is a fetch type, we can infer the goal based on this id to avoid large schemas in json",
        default=None,
    )
    evals: List[Eval] = Field(
        description="Various evaluations to test for within the example"
    )

    def get_static_url(self) -> str:
        from bananalyzer.runner.website_responder import get_website_responder

        return get_website_responder(self).get_url(self)

    @model_validator(mode="before")
    def set_goal_if_fetch_id_provided(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        from bananalyzer.data.fetch_schemas import get_fetch_schema

        goal_type = values.get("type")
        if goal_type != "fetch":
            return values

        fetch_id: Optional[FetchId] = values.get("fetch_id")
        goal = values.get("goal")

        if fetch_id is not None and goal is not None:
            raise ValueError("fetch_id and goal cannot both be provided")

        if fetch_id is None and goal is not None:
            return values

        if fetch_id is None:
            raise ValueError("fetch_id must be provided if goal is not provided")

        fetch_schema = get_fetch_schema(fetch_id)
        values["goal"] = (
            fetch_schema.model_fields
            if not isinstance(fetch_schema, dict)
            and issubclass(fetch_schema, BaseModel)
            else fetch_schema
        )

        return values
