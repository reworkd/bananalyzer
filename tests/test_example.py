from typing import Any, Dict, Optional

import pytest
from _pytest.outcomes import Failed
from pydantic import ValidationError

from bananalyzer.data.fetch_schemas import fetch_schemas
from bananalyzer.data.schemas import Eval, Example
from bananalyzer.runner.evals import format_new_lines


def test_format_new_lines() -> None:
    assert {"1": "one two"} == format_new_lines({"1": "one\ntwo"})
    assert {"1": "one two"} == format_new_lines({"1": "one two"})
    assert {"1": "one  two"} == format_new_lines({"1": "one\n\ntwo"})
    assert {"1": "one two", "2": "one two"} == format_new_lines(
        {"1": "one\ntwo", "2": "one\ntwo"}
    )
    assert {"1": "one two", "2": "one two"} == format_new_lines(
        {"1": "one two", "2": "one\ntwo"}
    )


def test_json_eval(mocker: Any) -> None:
    page = mocker.Mock()
    json = {"one": "one", "two": "two\ntwo"}
    evaluation = Eval(type="json_match", expected=json)

    # Exact match
    evaluation.eval_results(page, {"one": "one", "two": "two\ntwo"})

    # Order doesn't matter
    evaluation.eval_results(page, {"two": "two\ntwo", "one": "one"})

    # New lines converted into spaces
    evaluation.eval_results(page, {"two": "two two", "one": "one"})

    # Different values fail
    with pytest.raises(Failed):
        evaluation.eval_results(page, {"one": "one", "two": "different"})

    # Additional key-value pairs fail
    with pytest.raises(Failed):
        evaluation.eval_results(
            page, {"one": "one", "two": "two\ntwo", "three": "three"}
        )


def test_json_eval_ignores___attributes(mocker: Any) -> None:
    page = mocker.Mock()
    expected = {"one": "one", "none": None}
    evaluation = Eval(type="json_match", expected=expected)

    #  __attributes ignored
    __attributes_added = {
        "one": "one",
        "none": None,
        "__url": "https://www.test.com",
        "__zest": "test",
        "__blah": None,
    }
    evaluation.eval_results(page, __attributes_added)

    # Fail without __
    url_added = {"one": "one", "none": None, "url": "https://www.test.com"}
    with pytest.raises(Failed):
        evaluation.eval_results(page, url_added)


def test_json_eval_with_none_values(mocker: Any) -> None:
    page = mocker.Mock()
    expected = {"one": "one", "none": None}
    evaluation = Eval(type="json_match", expected=expected)

    # None attribute missing succeeds
    none_attribute_missing = {"one": "one"}
    evaluation.eval_results(page, none_attribute_missing)

    # None attribute correctly set to None
    actual_with_none = {"one": "one", "none": None}
    evaluation.eval_results(page, actual_with_none)

    # Key present with non None value fails
    actual_incorrect_value = {"one": "one", "two": "Available"}
    with pytest.raises(Failed):
        evaluation.eval_results(page, actual_incorrect_value)

    # Incorrect missing key fails
    missing_key = {"two": None}
    with pytest.raises(Failed):
        evaluation.eval_results(page, missing_key)


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
