import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Type

import pytest
from playwright.async_api import Page
from pydantic import BaseModel, Field, model_validator

from bananalyzer.runner.evals import (
    AllowedJSON,
    validate_end_url_match,
    validate_field_match,
    validate_json_match,
)

ExampleType = Literal[
    "listing",
    "detail",
    "listing_detail",
]

SchemaName = Literal[
    "job_posting",
    "manufacturing_commerce",
    "contact",
    "contract",
    "forum",
    "attorney",
    "attorney_job_listing",
]

PossibleTags = Literal[
    "regression",
    "single-output",
    "accordion",
    "pagination",
    "colliding-tags",
    "contract",
    "badly-formatted",
    "urls",
]


class Eval(BaseModel):
    """
    Base class for all evals. Evals are used to determine if an action or result is correct
    """

    type: Literal["json_match", "end_url_match"] = "json_match"
    expected: AllowedJSON | None = Field(default=None)
    options: Optional[list[AllowedJSON]] = Field(default=None)

    @model_validator(mode="before")
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
            except ValueError as e:
                exceptions.append(e)

        if len(exceptions) == len(options):
            if len(options) > 1:
                pytest.fail(
                    f"None of the available options matched. For example: {str(exceptions[0])}"
                )
            pytest.fail(str(exceptions[0]))


class Example(BaseModel):
    id: str
    url: str
    resource_path: Optional[str] = Field(
        description="Local path of a HAR, S3 URL of a HAR directory's tar.gz, or remote URL of MHTML",
        default=None,
    )
    source: Literal["mhtml", "hosted", "har"] = Field(
        description="Source of the website"
    )
    category: str = Field(description="Category of the website")
    subcategory: str = Field(description="Subcategory of the website")
    type: ExampleType = Field(description="The stage of the current page")
    goal: str = Field(description="The goal of the agent for this specific example")
    schema_: Dict[str, Any] = Field(
        description="The JSON schema of the data to be extracted"
    )
    evals: List[Eval] = Field(
        description="Various evaluations to test for within the example"
    )
    tags: List[Literal[PossibleTags]] = Field(default=[])

    def get_static_url(self) -> str:
        from bananalyzer.runner.website_responder import get_website_responder

        return get_website_responder(self).get_url(self)

    @property
    def har_file_path(self) -> Path:
        from bananalyzer.data.examples import get_examples_path

        if self.source != "har":
            raise ValueError("This example is not a HAR file")
        if not self.resource_path:
            raise ValueError("This example does not have a resource path")
        if not self.resource_path.startswith(
            "s3://"
        ) and not self.resource_path.endswith(".tar.gz"):
            return get_examples_path() / self.resource_path

        parts = self.resource_path.split("/")
        har_subpath = "/".join(parts[3:]).split(".")[0] + "/index.har"
        har_path = get_examples_path() / har_subpath

        if not os.path.exists(har_path):
            raise ValueError(
                f"Could not find HAR file at {har_path}. Please ensure it has been downloaded from S3 to the correct location."
            )

        return har_path

    @model_validator(mode="before")
    def set_schema_and_goal(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        from bananalyzer.data.fetch_schemas import get_fetch_schema, get_goal

        if values.get("schema_") is None:
            values["schema_"] = {"data": {"type": "object"}}

        schema_name = ""
        if type(values.get("schema_")) == str:
            schema_name = values["schema_"]
            values["schema_"] = get_fetch_schema(schema_name)

        if values.get("goal") is None:
            values["goal"] = get_goal(schema_name)

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
