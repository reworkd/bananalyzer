import json
import shutil
import subprocess
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

    return (path / train_examples_name).exists() and (
        path / test_examples_name
    ).exists()


def get_examples_path() -> Path:
    if are_examples_available(local_examples_path):
        print("### Using local examples! ###")
        return local_examples_path
    elif are_examples_available(downloaded_examples_path):
        return downloaded_examples_path
    else:
        raise FileNotFoundError(
            "No examples download. Re-run with `--download` to download example data via git."
        )


def download_examples() -> None:
    """
    Downloads the repo via git and places contents of the `/static` data directory in ~/.bananalyzer_data
    """
    repo_url = "https://github.com/reworkd/bananalyzer.git"
    branch = "main"
    data_folder_name = "static/"

    try:
        subprocess.run(
            ["git", "clone", "-b", branch, repo_url, "repo_temp"], check=True
        )

        data_folder_path = Path("repo_temp") / data_folder_name
        if not data_folder_path.exists():
            raise FileNotFoundError(
                f"The folder '{data_folder_name}' does not exist in the repository."
            )

        downloaded_examples_path.mkdir(parents=True, exist_ok=True)
        for item in downloaded_examples_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        for item in data_folder_path.iterdir():
            shutil.move(str(item), downloaded_examples_path)

    finally:
        print("Cleaning up repo...")
        shutil.rmtree("repo_temp", ignore_errors=True)


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
    return load_examples_at_path(get_examples_path(), train_examples_name)


def get_test_examples() -> List[Example]:
    return load_examples_at_path(get_examples_path(), test_examples_name)


def get_all_examples() -> List[Example]:
    return get_training_examples() + get_test_examples()


def get_all_example_urls() -> List[str]:
    return [example.url for example in get_all_examples()]


def get_example_by_url(url: str) -> Example:
    for example in get_all_examples():
        if example.url == url:
            return example
    raise ValueError(f"No example found with URL: {url}")
