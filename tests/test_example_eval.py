from typing import Any, Dict, Optional

import pytest
from _pytest.outcomes import Failed
from pytest_mock import MockFixture

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


def test_json_eval_field(mocker: MockFixture) -> None:
    page = mocker.Mock()
    json = {
        "first_name": "Brett",
        "last_name": "Olavage",
        "title": "Specialist",
        "email": None,
    }
    evaluation = Eval(type="json_match", expected=json)

    evaluation.eval_results(
        page, {"last_name": "Olavage"}, field="last_name"
    )  # Exact match
    evaluation.eval_results(
        page, {"last_name": "Olavage\n"}, field="last_name"
    )  # With new line
    evaluation.eval_results(page, {"email": ""}, field="email")  # With new line


def test_json_eval_1(mocker: MockFixture) -> None:
    page = mocker.Mock()
    json = {"one": "one", "two": "two\ntwo", "three": None}
    evaluation = Eval(type="json_match", expected=json)

    # Exact match
    evaluation.eval_results(page, {"one": "one", "two": "two\ntwo", "three": None})

    # Order doesn't matter
    evaluation.eval_results(page, {"two": "two\ntwo", "one": "one", "three": None})

    # New lines converted into spaces
    evaluation.eval_results(page, {"two": "two two", "one": "one", "three": None})

    # Added new lines don't matter
    evaluation.eval_results(page, {"two": "two two", "one": "one\n", "three": None})

    # Empty space is same as None
    evaluation.eval_results(page, {"two": "two two", "one": "one\n", "three": ""})

    # Different values fail
    with pytest.raises(Failed):
        evaluation.eval_results(page, {"one": "one", "two": "different", "three": None})

    # Additional key-value pairs fail
    with pytest.raises(Failed):
        evaluation.eval_results(
            page, {"one": "one", "two": "two\ntwo", "three": None, "four": "four"}
        )


def test_only_one_of_expected_or_options_can_be_provided() -> None:
    # Works fine
    Eval(type="json_match", expected={"1": "1"}).dict()
    Eval(type="json_match", options=[{"2": "2"}]).dict()

    # Both provided
    with pytest.raises(ValueError):
        Eval(type="json_match", expected={"1": "1"}, options=[{"2": "2"}])

    # Neither provided
    with pytest.raises(ValueError):
        Eval(type="json_match").dict()


def test_json_eval_options(mocker: MockFixture) -> None:
    page = mocker.Mock()
    options = [{"1": "1"}, {"2": "2"}]
    evaluation = Eval(type="json_match", options=options)

    # Either option works
    evaluation.eval_results(page, {"1": "1"})
    evaluation.eval_results(page, {"2": "2"})

    # Non matching option fails
    with pytest.raises(Failed):
        evaluation.eval_results(page, {"3": "3"})


def test_json_eval_ignores___attributes(mocker: MockFixture) -> None:
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


def test_json_eval_with_none_values(mocker: MockFixture) -> None:
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


def test_url_eval(mocker: MockFixture) -> None:
    expected_url = "https://www.test.com"
    page = mocker.Mock()
    page.url = expected_url

    Eval(type="end_url_match", expected=expected_url).eval_results(page, {})
    with pytest.raises(Failed):
        Eval(
            type="end_url_match", expected="https://www.failure_case.com"
        ).eval_results(page, {})


def create_default_example(
    overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    default_example: Dict[str, Any] = {
        "id": "1",
        "url": "url",
        "source": "mhtml",
        "category": "category",
        "subcategory": "subcategory",
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


def test_fetch_with_goal_and_no_fetch_id() -> None:
    goal = {"test": "test"}
    example_data = create_default_example({"goal": goal})
    example = Example(**example_data)
    assert example.goal == goal


def test_fetch_with_non_dictionary_goal() -> None:
    goal = "THIS SHOULD BE FINE"
    example_data = create_default_example({"goal": goal})
    example = Example(**example_data)
    assert example.goal == goal
