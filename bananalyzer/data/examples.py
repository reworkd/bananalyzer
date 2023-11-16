import json
from pathlib import Path
from typing import Any, Dict, List

from bananalyzer.data.schemas import Example

# Load example paths
training_examples_path: Path = Path(__file__).resolve().parent / "examples.json"
test_examples_path: Path = Path(__file__).resolve().parent / "test_examples.json"
with open(training_examples_path, "r", encoding="utf-8") as file:
    training_example_jsons: List[Dict[str, Any]] = json.load(file)
with open(test_examples_path, "r", encoding="utf-8") as file:
    test_example_jsons: List[Dict[str, Any]] = json.load(file)

training_examples: List[Example] = [
    Example(**example) for example in training_example_jsons
]
test_examples: List[Example] = [Example(**example) for example in test_example_jsons]


def get_all_example_urls() -> List[str]:
    return [example.url for example in training_examples + test_examples]


def get_example_by_url(url: str) -> Example:
    matching_examples = [
        example for example in training_examples + test_examples if example.url == url
    ]
    if len(matching_examples) != 1:
        raise ValueError(
            f"Expected 1 matching example, got {len(matching_examples)}: {matching_examples}"
        )
    return matching_examples[0]


def get_examples_path() -> Path:
    return test_examples_path.parent
