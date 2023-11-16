from typing import Any, Dict, Optional

import pytest
from _pytest.outcomes import Failed
from pydantic import ValidationError

from bananalyzer.data.fetch_schemas import fetch_schemas
from bananalyzer.data.schemas import Eval, Example


def test_json_eval(mocker: Any) -> None:
    page = mocker.Mock()
    json = {"one": "one", "two": "two"}

    evaluation = Eval(type="json_match", expected=json)

    evaluation.eval_results(page, json)
    evaluation.eval_results(page, {"two": "two", "one": "one"})
    with pytest.raises(Failed):
        evaluation.eval_results(page, {"test": "test"})


def test_url_eval(mocker: Any) -> None:
    expected_url = "https://www.test.com"
    page = mocker.Mock()
    page.url = expected_url

    Eval(type="end_url_match", expected=expected_url).eval_results(page, {})
    with pytest.raises(Failed):
        Eval(
            type="end_url_match", expected="https://www.failure_case.com"
        ).eval_results(page, {})


def create_default_example(
    overrides: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    default_example: Dict[str, Any] = {
        "id": "1",
        "url": "url",
        "source": "mhtml",
        "domain": "domain",
        "subdomain": "subdomain",
        "type": "fetch",
        "evals": [],
        "fetch_id": None,  # Set as None by default
        "goal": None,  # Set as None by default
    }
    if overrides:
        default_example.update(overrides)
    return default_example


def test_non_fetch_with_goal() -> None:
    example_data = create_default_example({"type": "multiple", "goal": "goal"})
    Example(**example_data)


def test_fetch_without_fetch_id_exception() -> None:
    example_data = create_default_example({"type": "fetch", "fetch_id": None})
    # Since fetch_id is None by default, no need to override it
    with pytest.raises(Exception):
        Example(**example_data)


def test_fetch_with_fetch_id_and_goal_should_raise_validation_error() -> None:
    example_data = create_default_example(
        {
            "fetch_id": "job_posting",
            "goal": "goal",
        }
    )
    with pytest.raises(ValidationError):
        Example(**example_data)


def test_fetch_with_fetch_id_and_no_goal_sets_default_goal() -> None:
    example_data = create_default_example({"fetch_id": "job_posting", "goal": None})
    example = Example(**example_data)
    assert example.goal == fetch_schemas["job_posting"]
