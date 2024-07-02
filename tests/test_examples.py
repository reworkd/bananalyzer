import json
import os
import shutil
from pathlib import Path
from typing import List
from unittest.mock import mock_open

import pytest
from pytest_mock import MockFixture

from bananalyzer.data.examples import (
    download_examples,
    downloaded_examples_path,
    get_all_examples,
    get_example_by_url,
    get_examples_path,
    get_test_examples,
    get_training_examples,
    load_examples_at_path,
    local_examples_path,
)
from bananalyzer.data.schemas import Example


def test_load_examples_at_path_success(mocker: MockFixture) -> None:
    data: List[Example] = []
    mocker.patch("builtins.open", mock_open(read_data=json.dumps(data)))
    loaded_examples = load_examples_at_path(Path("/fake/path"), "fake.json")
    assert len(loaded_examples) == len(data)
    assert all(isinstance(example, Example) for example in loaded_examples)


def test_load_examples_at_path_json_error(mocker: MockFixture) -> None:
    mocker.patch("builtins.open", mock_open(read_data="invalid json"))
    with pytest.raises(json.JSONDecodeError):
        load_examples_at_path(Path("/fake/path"), "fake.json")


def test_load_examples_at_path_file_not_found(mocker: MockFixture) -> None:
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        load_examples_at_path(Path("/fake/path"), "fake.json")


def test_get_local_examples_path() -> None:
    # Running test in repo will default to local path
    assert get_examples_path() == local_examples_path


def test_get_examples_path_failure(mocker: MockFixture) -> None:
    mocker.patch("pathlib.Path.exists", return_value=False)

    with pytest.raises(FileNotFoundError):
        get_examples_path()


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Do not download 100MB dataset on GitHub Actions",
)
def test_download_examples() -> None:
    if downloaded_examples_path.exists():
        shutil.rmtree(downloaded_examples_path)

    download_examples()

    assert downloaded_examples_path.exists(), "Downloaded examples path does not exist."
    assert any(downloaded_examples_path.iterdir()), "Downloaded examples path is empty."


##########################################################
# The following tests use examples in the static folder. #
##########################################################
def test_get_example_by_url_not_found() -> None:
    with pytest.raises(ValueError):
        get_example_by_url("http://nonexistent.com")


def test_get_example_with_known_id() -> None:
    assert (
        get_example_by_url("https://www.uwmedicine.org/locations/northwest-hospital").id
        == "MRD347sMiS2vlw091LAqK"
    )


def test_get_examples() -> None:
    training_examples = get_training_examples()
    test_examples = get_test_examples()

    assert training_examples + test_examples == get_all_examples()
