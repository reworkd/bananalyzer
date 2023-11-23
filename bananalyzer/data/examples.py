import json
from pathlib import Path
from typing import Any, Dict, List

from bananalyzer.data.schemas import Example

local_examples_path: Path = Path(__file__).resolve().parent.parent.parent / "static"
downloaded_examples_path: Path = Path("TODO").resolve()
train_examples_name = "examples.json"
test_examples_name = "test_examples.json"


def are_examples_available(path: Path) -> bool:
    if not path.exists():
        return False

    # Validate train and test set available
    return (path / train_examples_name).exists() and (
        path / test_examples_name
    ).exists()


def get_examples_path() -> Path:
    if are_examples_available(local_examples_path):
        print("### Returning local examples ###")
        return local_examples_path
    return downloaded_examples_path


def download_examples() -> None:
    pass


def load_examples_at_path(path: Path, examples_json_file_name: str) -> List[Example]:
    examples_json_path = path / examples_json_file_name
    with open(examples_json_path, "r") as file:
        example_jsons: List[Dict[str, Any]] = json.load(file)
    return [Example(**example) for example in example_jsons]


def get_training_examples() -> List[Example]:
    examples_path = get_examples_path()
    return load_examples_at_path(examples_path, train_examples_name)


def get_test_examples() -> List[Example]:
    examples_path = get_examples_path()
    return load_examples_at_path(examples_path, test_examples_name)

 
def get_all_examples() -> List[Example]:
    return get_training_examples() + get_test_examples()


def get_all_example_urls() -> List[str]:
    return [example.url for example in get_all_examples()]


def get_example_by_url(url: str) -> Example:
    matching_examples = [
        example for example in get_all_examples() if example.url == url
    ]
    if len(matching_examples) != 1:
        raise ValueError(
            f"Expected 1 matching example, got {len(matching_examples)}: {matching_examples}"
        )
    return matching_examples[0]
