import json
from typing import Any, Dict, List, Literal, Optional, Union

import pytest
from deepdiff import DeepDiff
from playwright.async_api import Page
from pydantic import BaseModel, Field, model_validator

from bananalyzer.data.fetch_schemas import fetch_schemas

GoalType = Literal[
    "fetch",  # Scrape specific JSON information from a single page. Does not require navigation
    "links",  # Scrape all detail page links from a single page
    "click",  # Make a single click on a page
    "navigate",  # Travel to a new page
    "search",  # Search for the answer to a specific query
    "multiple",  # Perform multiple intents
]


def format_new_lines(d: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively replace newlines in strings with spaces."""
    new_dict: Dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            new_dict[k] = format_new_lines(v)
        elif isinstance(v, str):
            new_dict[k] = v.replace("\n", " ")
        else:
            new_dict[k] = v
    return new_dict


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

    def eval_results(self, page: Page, result: Dict[str, Any]) -> None:
        if self.type == "json_match":
            assert isinstance(self.expected, dict)

            # TODO: We should probably code gen to remove newlines or update test data to contain new lines
            formatted_expected = format_new_lines(self.expected)
            formatted_actual = format_new_lines(result)

            # TODO: Pass in schema in the backend and handle this OUTSIDE of tests
            # Adding missing keys in actual with None if they are expected to be None
            for key, value in formatted_expected.items():
                if value is None and key not in formatted_actual:
                    formatted_actual[key] = None

            diff = DeepDiff(
                formatted_expected,
                formatted_actual,
                ignore_order=True,
                report_repetition=True,
            )
            if diff:
                # Pretty print both expected and actual results
                pretty_expected = json.dumps(formatted_expected, indent=4)
                pretty_actual = json.dumps(formatted_actual, indent=4)

                diff_msg = f"Actual: {pretty_actual}\nExpected: {pretty_expected}"
                pytest.fail(f"JSONEval mismatch!\n{diff_msg}")

        elif self.type == "end_url_match":
            if page.url != self.expected:
                diff_msg = f"Actual URL:\t{page.url}\nExpected URL:\t{self.expected}"
                pytest.fail(f"URLEval mismatch!\n{diff_msg}")


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
        Literal["job_posting", "manufacturing_commerce", "contact"]
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

        values["goal"] = fetch_schemas[fetch_id]
        return values
