import pytest

from bananalyzer.runner.evals import sanitize_string, validate_field_match


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("hello world!", "helloworld"),
        ("HELLO_WORLD", "helloworld"),
        ("Hello1 WoRlD@!", "hello1world"),
        ("", ""),
        ("123456", "123456"),
        ("!@#$%^&*()", ""),
        ("Hello World 123", "helloworld123"),
        ("     ", ""),
        ("HELLO", "hello"),
        ("hello", "hello"),
        ("HelloWorld2023", "helloworld2023"),
    ],
)
def test_sanitize_string(input_str, expected):
    assert sanitize_string(input_str) == expected


@pytest.mark.parametrize(
    "expected, actual, field",
    [
        ({"field": "TestValue123"}, {"field": "test value!123"}, "field"),
        ({"field": "AnotherTest123"}, {"field": "another test 123"}, "field"),
        ({"field": ""}, {"field": " "}, "field"),
    ],
)
def test_validate_field_match(expected, actual, field):
    validate_field_match(expected, actual, field)


@pytest.mark.parametrize(
    "expected, actual, field",
    [
        ({"field": "TestValue123"}, {"field": "DifferentValue123"}, "field"),
        ({"field": None}, {"field": "testvalue"}, "field"),
        ({"field": "Value"}, {"other_field": "Value"}, "field"),
    ],
)
def test_validate_field_match_fail(expected, actual, field):
    with pytest.raises(pytest.fail.Exception):
        validate_field_match(expected, actual, field)
