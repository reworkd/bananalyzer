import json
from typing import Any, Dict, List, Literal, Optional, Type, Union

import pytest
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
    expected: AllowedJSON | None = Field(default=None)
    options: Optional[AllowedJSON] = Field(default=None)

    @model_validator(mode='before')
    def validate_expected_or_options(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        expected = values.get("expected")
        options = values.get("options")

        if expected is not None and options is not None:
            raise ValueError("Only one of expected or options can be provided")

        if expected is None and options is None:
            raise ValueError("One of expected or options must be provided")

        return values

    def eval_action(self, action: str) -> bool:
        """
        We don't care for action level evals at the moment
        """
        raise NotImplementedError("eval_action not implemented")

    def eval_results(
        self, page: Page, result: Dict[str, Any], field: Optional[str] = None
    ) -> None:
        if self.type == "json_match":
            return self.handle_json_match(result, field)

        if self.type == "end_url_match" and isinstance(self.expected, str):
            return validate_end_url_match(self.expected, page.url)

        raise NotImplementedError("No evaluation type implemented")

    def handle_json_match(self, result: Dict[str, Any], field: Optional[str]) -> None:
        options = self.options or [self.expected]
        exceptions: list[ValueError] = []

        # Try all options
        for option in options:
            try:
                if (
                    self.type == "json_match"
                    and field is not None
                    and isinstance(option, dict)
                ):
                    return validate_field_match(option, result, field)

                if self.type == "json_match" and isinstance(option, (list, dict)):
                    return validate_json_match(option, result)
            except Exception as e:
                exceptions.append(e)

        if len(exceptions) == len(options):
            if len(options) > 1:
                pytest.fail(f"None of the available options matched. For example: {str(exceptions[0])}")
            pytest.fail(str(exceptions[0]))


FetchId = Literal[
    "job_posting",
    "manufacturing_commerce",
    "contact",
    "contract",
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
    tags: List[str] = Field(default=[])

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
            json.dumps(model_to_dict(fetch_schema), indent=4)
            if not isinstance(fetch_schema, Dict)
            and issubclass(fetch_schema, BaseModel)
            else fetch_schema
        )

        # TODO: Fix this hack and construct all common goals from code and place schema in a different attribute
        from bananalyzer.data.fetch_schemas import CONTACT_SCHEMA_GOAL

        if fetch_id == "contact":
            values["goal"] = (
                f"{CONTACT_SCHEMA_GOAL} Return data in the following schema:\n"
                + str(values["goal"])
            )
        from bananalyzer.data.fetch_schemas import GOVERNMENT_CONTRACT_GOAL

        if fetch_id == "contract":
            values["goal"] = (
                f"{GOVERNMENT_CONTRACT_GOAL} Return data in the following schema:\n"
                + str(values["goal"])
            )

        return values


def model_to_dict(model: Type[BaseModel]) -> Dict[str, Any]:
    result = {}
    for name, field in model.model_fields.items():
        if not field.annotation:
            continue
        if (
            field.annotation.__name__.lower() == "list"
            and len(field.annotation.__args__) == 1
        ):
            inner_type = field.annotation.__args__[0]
            if issubclass(inner_type, BaseModel):
                result[name] = {
                    "type": f"List[{inner_type.__name__}]",
                    "items": {
                        "type": "object",
                        "properties": model_to_dict(inner_type),
                    },
                }
            else:
                result[name] = {
                    "type": f"List[{inner_type.__name__}]",
                }
        elif issubclass(field.annotation, BaseModel):
            result[name] = {
                "type": "object",
                "properties": model_to_dict(field.annotation),
            }
        else:
            result[name] = {
                "type": field.annotation.__name__ if field.annotation else "Any",
            }

        if field.description:
            result[name]["description"] = field.description
    return result
