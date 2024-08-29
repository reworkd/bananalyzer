import pytest

from bananalyzer.runner.evals import sort_keys_based_on_expected


@pytest.mark.parametrize(
    "actual, expected, result",
    [
        # Basic dictionary sorting
        ({"b": 2, "a": 1, "c": 3}, {"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}),
        # Nested dictionaries
        (
            {"b": {"y": 2, "x": 1}, "a": 1, "c": 3},
            {"a": 1, "b": {"x": 1, "y": 2}},
            {"a": 1, "b": {"x": 1, "y": 2}, "c": 3},
        ),
        # Lists within dictionaries
        ({"b": [3, 2, 1], "a": 1}, {"a": 1, "b": [1, 2]}, {"a": 1, "b": [3, 2, 1]}),
        # Lists of dictionaries
        (
            [{"b": 2, "a": 1, "c": 3}, {"e": 5, "d": 4, "f": 6}],
            [{"a": 1, "b": 2}, {"d": 4, "e": 5}],
            [{"a": 1, "b": 2, "c": 3}, {"d": 4, "e": 5, "f": 6}],
        ),
        # Missing keys in actual
        ({"b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}, {"a": None, "b": 2, "c": 3}),
        # Extra keys in actual
        (
            {"b": 2, "a": 1, "c": 3, "d": 4},
            {"a": 1, "b": 2},
            {"a": 1, "b": 2, "c": 3, "d": 4},
        ),
        # Different types (string)
        ("actual", "expected", "actual"),
        # Different types (integer)
        (42, 100, 42),
        # None values
        ({"b": 2, "a": None}, {"a": 1, "b": None}, {"a": None, "b": 2}),
        # Empty structures
        ({}, {"a": 1, "b": 2}, {"a": None, "b": None}),
        # Lists of different lengths
        ([1, 2, 3, 4], [4, 5, 6], [1, 2, 3, 4]),
        # Nested structures with lists of different lengths
        (
            {"b": {"x": [5, 6, 7]}, "a": [1, 2, 3, 4]},
            {"a": [4, 5], "b": {"x": [7, 8, 9, 10]}},
            {"a": [1, 2, 3, 4], "b": {"x": [5, 6, 7]}},
        ),
        # Mixed types in lists
        (
            [{"three": 3}, [4, 5], 1, "two"],
            [1, 2, {"three": 3}, [4, 5, 6]],
            [{"three": 3}, [4, 5], 1, "two"],
        ),
        # Deeply nested structures
        (
            {"a": {"b": {"c": {"d": [1, 2, 3]}}}},
            {"a": {"b": {"c": {"d": [4, 5]}}}},
            {"a": {"b": {"c": {"d": [1, 2, 3]}}}},
        ),
        # Actual is None
        (None, {"a": 1, "b": 2}, None),
        # Expected is None
        ({"a": 1, "b": 2}, None, {"a": 1, "b": 2}),
    ],
)
def test_sort_keys_based_on_expected(actual, expected, result):
    assert sort_keys_based_on_expected(actual, expected) == result


def test_sort_keys_based_on_expected_with_large_nested_structure():
    actual = {
        "users": [
            {"id": 1, "name": "Alice", "age": 30, "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "age": 25, "phone": "1234567890"},
            {
                "id": 3,
                "name": "Charlie",
                "age": 35,
                "address": {"city": "New York", "country": "USA"},
            },
        ],
        "products": [
            {"id": 101, "name": "Laptop", "price": 1000, "stock": 50},
            {"id": 102, "name": "Phone", "price": 500, "features": ["5G", "Dual SIM"]},
        ],
        "settings": {
            "theme": "dark",
            "notifications": True,
            "language": "en",
        },
    }
    expected = {
        "users": [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35, "address": {"city": "New York"}},
        ],
        "products": [
            {"id": 101, "name": "Laptop", "price": 1000},
            {"id": 102, "name": "Phone", "price": 500},
        ],
        "settings": {
            "theme": "light",
            "notifications": False,
        },
    }
    result = sort_keys_based_on_expected(actual, expected)
    assert result == {
        "users": [
            {"id": 1, "name": "Alice", "age": 30, "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "age": 25, "phone": "1234567890"},
            {
                "id": 3,
                "name": "Charlie",
                "age": 35,
                "address": {"city": "New York", "country": "USA"},
            },
        ],
        "products": [
            {"id": 101, "name": "Laptop", "price": 1000, "stock": 50},
            {"id": 102, "name": "Phone", "price": 500, "features": ["5G", "Dual SIM"]},
        ],
        "settings": {
            "theme": "dark",
            "notifications": True,
            "language": "en",
        },
    }


def test_sort_keys_based_on_expected_with_empty_structures():
    actual = {"a": [], "b": {}, "c": [1, 2, 3], "d": {"x": 1}}
    expected = {"a": [1, 2], "b": {"y": 2}, "c": [], "d": {}}
    result = sort_keys_based_on_expected(actual, expected)
    assert result == {"a": [], "b": {"y": None}, "c": [1, 2, 3], "d": {"x": 1}}


def test_sort_keys_based_on_expected_with_different_types():
    actual = {"a": 1, "b": "string", "c": [1, 2, 3], "d": {"x": 1}}
    expected = {"a": "one", "b": 2, "c": {"y": 2}, "d": [1, 2, 3]}
    result = sort_keys_based_on_expected(actual, expected)
    assert result == {"a": 1, "b": "string", "c": [1, 2, 3], "d": {"x": 1}}
