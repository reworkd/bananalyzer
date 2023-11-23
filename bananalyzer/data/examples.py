import json
from pathlib import Path
from typing import List

from bananalyzer.data.schemas import Example

local_examples_path: Path = Path(__file__).resolve().parent.parent.parent / "static"
downloaded_examples_path = Path.home() / ".bananalyzer_data"
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
    try:
        with open(examples_json_path, "r") as file:
            example_jsons = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {examples_json_path}: {e}")
        raise
    except FileNotFoundError as e:
        print(f"Example file not found: {e}")
        raise

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
    for example in get_all_examples():
        if example.url == url:
            return example
    raise ValueError(f"No example found with URL: {url}")
