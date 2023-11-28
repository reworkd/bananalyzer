import pytest

from bananalyzer.runner.evals import (
    is_string_similar,
    sanitize_string,
    validate_field_match,
)


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
    "actual, expected, tolerance, expected_result",
    [
        ("Hello-World", "hello world", 2, True),
        ("test123", "test!123", 2, True),
        ("string-with-chars", "stringwithchars", 2, True),
        ("text_with_underscores", "textwithunderscores", 2, True),
        ("hello", "he-llo", 1, True),
        ("string", "string!!", 2, True),
        ("foo", "foo--", 2, True),
        ("short", "s-h-o-r-t", 2, False),
        ("text", "text----", 2, False),
        ("word", "w-o-r-d-e", 3, False),
        ("name", "n-a-m-e--", 3, False),
        ("different", "diff3r3nt", 2, False),
        ("text", "txet", 2, False),
        ("hello", "world", 2, False),
        ("abc", "def", 2, False),
        ("example", "ex-ample", 0, False),
        ("", "", 2, True),
        ("a", "a-", 1, True),
        ("b", "b--", 1, False),
        ("c+", "c-", 0, False),
        ("d---", "d+++", 1, False),
        ("++e+++", "---e--", 0, False),
        ("615 Douglas Street, Suite 500 Durham, NC 27705",
         "615 Douglas Street, Suite 500, Durham, NC 27705", 2, True),
        ("615 Douglas Street, \n\n'Suite 500 Durham', NC 27-705",
         "615 Douglas Street, Suite 500, Durham, NC 27705", 2, True),
    ],
)
def test_is_string_similar(actual, expected, tolerance, expected_result):
    assert is_string_similar(actual, expected, tolerance) == expected_result


@pytest.mark.parametrize(
    "expected, actual, field",
    [
        ({"field": "Hello World"}, {"field": "Hello-World"}, "field"),
        ({"field": "test"}, {"field": "test!!"}, "field"),
        ({"field": 123}, {"field": 123}, "field"),
        ({"field": [1, 2, 3]}, {"field": [1, 2, 3]}, "field"),
    ],
)
def test_validate_field_match_pass(expected, actual, field):
    validate_field_match(expected, actual, field)


@pytest.mark.parametrize(
    "expected, actual, field",
    [
        ({"field": "example"}, {"field": "example 123"}, "field"),
        ({"field": "short string"}, {"field": "short string!!!"}, "field"),
        ({"field": [1, 2, 3]}, {"field": [1, 2]}, "field"),
    ],
)
def test_validate_field_match_fail(expected, actual, field):
    with pytest.raises(pytest.fail.Exception):
        validate_field_match(expected, actual, field)
