from pathlib import Path
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
        "last_name": "Savage",
        "title": "Specialist",
        "email": None,
    }
    evaluation = Eval(type="json_match", expected=json)

    evaluation.eval_results(
        page, {"last_name": "Savage"}, field="last_name"
    )

    evaluation.eval_results(
        page, {"last_name": "Savage\n"}, field="last_name"
    )

    evaluation.eval_results(page, {"email": ""}, field="email")


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


def test_json_eval_lists(mocker: MockFixture) -> None:
    json = [{"key": "one\none"}, {"key": "two"}, {"key": "three"}]
    evaluation = Eval(type="json_match", expected=json)

    # Exact match
    evaluation.handle_json_match(json, field=None)

    # Order doesn't matter
    evaluation.handle_json_match([{"key": "three"}, {"key": "one\none"}, {"key": "two"}], field=None)

    # New lines converted into spaces
    evaluation.handle_json_match([{"key": "one one"}, {"key": "two"}, {"key": "three"}], field=None)

    # Added new lines don't matter
    evaluation.handle_json_match([{"key": "one\none"}, {"key": "two"}, {"key": "three\n"}], field=None)

    # Different values in list
    with pytest.raises(Failed):
        evaluation.handle_json_match([{"key": "one\none"}, {"key": "two"}, {"key": "four"}], field=None)

    # Having additional list items fails
    with pytest.raises(Failed):
        evaluation.handle_json_match(
            [{"key": "one\none"}, {"key": "two"}, {"key": "three"}, {"key": "four"}], field=None,
        )

    # Too few list items fails
    with pytest.raises(Failed):
        evaluation.handle_json_match(
            [{"key": "one\none"}, {"key": "two"}], field=None
        )


def test_only_one_of_expected_or_options_can_be_provided() -> None:
    # Works fine
    Eval(type="json_match", expected={"1": "1"}).model_dump()
    Eval(type="json_match", options=[{"2": "2"}]).model_dump()

    # Both provided
    with pytest.raises(ValueError):
        Eval(type="json_match", expected={"1": "1"}, options=[{"2": "2"}])

    # Neither provided
    with pytest.raises(ValueError):
        Eval(type="json_match").model_dump()


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
        "type": "detail",
        "evals": [],
        "schema_": None,  # Set as None by default
        "goal": None,  # Set as None by default
    }
    if overrides:
        default_example.update(overrides)
    return default_example


def test_no_goal_and_no_schema_set_defaults() -> None:
    example_data = create_default_example()
    example = Example(**example_data)
    assert example.goal and example.schema_


def test_with_goal_and_no_schema() -> None:
    goal = "this is my goal"
    example_data = create_default_example({"goal": goal})
    example = Example(**example_data)
    assert example.goal == goal


def test_with_schema_and_no_goal() -> None:
    schema = {"key": "value"}
    example_data = create_default_example({"schema_": schema})
    example = Example(**example_data)
    assert example.schema_ == schema


def test_with_schema_name() -> None:
    schema_name = "job_posting"
    example_data = create_default_example({"schema_": schema_name})
    example = Example(**example_data)
    assert isinstance(example.schema_, dict)


def test_goal_non_str() -> None:
    example_data = create_default_example({"goal": {"this goal": "is a dict"}})
    with pytest.raises(Exception):
        Example(**example_data)


@pytest.mark.parametrize(
    "overrides, expected_path",
    [
        # Test valid local HAR file path
        (
            {"resource_path": "example.har", "source": "har"},
            Path("path/to/example.har"),
        ),
        # Test valid S3 path with nested directories
        (
            {
                "resource_path": "s3://bucket_name/dir1/dir2/example.tar.gz",
                "source": "har",
            },
            Path("path/to/dir1/dir2/example/index.har"),
        ),
    ],
)
def test_har_file_path_valid(overrides, expected_path, mocker):
    mocker.patch(
        "bananalyzer.data.examples.get_examples_path", return_value=Path("path/to")
    )
    mocker.patch("os.path.exists", return_value=True)

    example_data = create_default_example(overrides)
    example_data["schema_"] = "job_posting"
    example = Example(**example_data)
    assert example.har_file_path == expected_path


@pytest.mark.parametrize(
    "overrides",
    [
        # Test non-HAR source with HAR file path
        {"resource_path": "example.har", "source": "mhtml"},
        # Test missing resource path
        {"resource_path": None, "source": "har"},
        # Test minimal S3 bucket path
        {"resource_path": "s3://bucket_name/", "source": "har"},
        # Test empty resource path
        {"resource_path": "", "source": "har"},
    ],
)
def test_har_file_path_invalid(overrides, mocker):
    mocker.patch(
        "bananalyzer.data.examples.get_examples_path", return_value=Path("path/to")
    )
    mocker.patch("os.path.exists", return_value=False)

    example_data = create_default_example(overrides)
    example_data["schema_"] = "job_posting"
    example = Example(**example_data)
    with pytest.raises(ValueError):
        _ = example.har_file_path
