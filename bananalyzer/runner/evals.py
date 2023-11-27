import json
import re
from typing import Any, Dict

import pytest
from deepdiff import DeepDiff

Result = Dict[str, Any]
NON_ALPHANUMERIC_PATTERN = re.compile(r"[^a-zA-Z0-9]")


def validate_field_match(expected: Result, actual: Result, field: str) -> None:
    expected_value = expected.get(field, None)
    actual_value = actual.get(field, None)

    sanitized_expected = (
        sanitize_string(str(expected_value)) if expected_value is not None else None
    )
    sanitized_actual = (
        sanitize_string(str(actual_value)) if actual_value is not None else None
    )

    if sanitized_expected != sanitized_actual:
        diff_msg = f"Actual: {actual_value}\nExpected: {expected_value}"
        pytest.fail(f"FieldEval mismatch!\n{diff_msg}")


def validate_json_match(expected: Result, actual: Result) -> None:
    assert isinstance(expected, dict)

    # TODO: We should probably code gen to remove newlines or update test data to contain new lines
    formatted_expected = format_new_lines(expected)
    formatted_actual = format_new_lines(actual)

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


def validate_end_url_match(expected: str, actual: str) -> None:
    if actual != expected:
        diff_msg = f"Actual URL:\t{actual}\nExpected URL:\t{expected}"
        pytest.fail(f"URLEval mismatch!\n{diff_msg}")


def sanitize_string(input_str: str) -> str:
    """Remove non-alphanumeric characters and convert to lowercase."""

    sanitized = NON_ALPHANUMERIC_PATTERN.sub("", input_str)
    return sanitized.lower()


def format_new_lines(d: Result) -> Result:
    """Recursively replace newlines in strings with spaces."""
    new_dict: Result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            new_dict[k] = format_new_lines(v)
        elif isinstance(v, str):
            new_dict[k] = v.replace("\n", " ")
        else:
            new_dict[k] = v
    return new_dict
