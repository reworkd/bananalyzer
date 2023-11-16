from typing import Any, Dict, Optional

import pytest
from _pytest.outcomes import Failed
from pydantic import ValidationError

from bananalyzer.data.fetch_schemas import get_fetch_schema
from bananalyzer.data.schemas import Example, JSONEval


def test_json_eval() -> None:
    json = {"one": "one", "two": "two"}

    eval = JSONEval(expected=json)

    eval.eval_results(json)
    eval.eval_results({"two": "two", "one": "one"})
    with pytest.raises(Failed):
        eval.eval_results({"test": "test"})


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
    example_data = create_default_example({"fetch_id": "contact", "goal": None})
    example = Example(**example_data)
    print(get_fetch_schema("contact").model_json_schema())
    assert example.goal == get_fetch_schema("contact").model_json_schema()
