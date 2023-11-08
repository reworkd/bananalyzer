import json
from pathlib import Path
from typing import Dict, Any, List

from bananalyzer.data.schemas import Example

examples_path: Path = Path(__file__).resolve().parent / "examples.json"

with open(examples_path, "r", encoding="utf-8") as file:
    example_jsons: List[Dict[str, Any]] = json.load(file)

examples: List[Example] = [Example(**example) for example in example_jsons]


def get_all_example_urls() -> List[str]:
    return [example.url for example in examples]


def get_example_by_url(url: str) -> Example:
    matching_examples = [example for example in examples if example.url == url]
    if len(matching_examples) != 1:
        raise ValueError(
            f"Expected 1 matching example, got {len(matching_examples)}: {matching_examples}"
        )
    return matching_examples[0]


def get_examples_path() -> Path:
    return examples_path.parent
