import json
import os
import shutil
import tarfile
from io import BytesIO
from pathlib import Path
from typing import List
from unittest.mock import mock_open

import pytest
from pytest_mock import MockFixture

from bananalyzer.data.banana_seeds import download_har
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
from bananalyzer.data.fetch_schemas import get_fetch_schema, get_goal
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


@pytest.fixture
def mock_s3_client(mocker):
    mock = mocker.patch("boto3.client")
    mock_instance = mock.return_value

    def prepare_tar_buffer(contents):
        tar_buffer = BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
            for content in contents:
                tarinfo = tarfile.TarInfo(name=content["name"])
                tarinfo.size = len(content["data"])
                tar.addfile(tarinfo, BytesIO(content["data"]))
        tar_buffer.seek(0)
        return tar_buffer

    return mock_instance, prepare_tar_buffer


@pytest.mark.parametrize(
    "contents",
    [
        [{"name": "index.har", "data": b"dummy har content"}],
        [{"name": "largefile.bin", "data": b"x" * 10**6}],
    ],
)
def test_download_har_write(mocker, mock_s3_client, contents):
    mock_instance, prepare_tar_buffer = mock_s3_client
    tar_buffer = prepare_tar_buffer(contents)
    mock_instance.get_object.return_value = {"Body": tar_buffer}

    har_dir_path = "/tmp/fake/dir"
    s3_url = "s3://test-bucket/test_har.tar.gz"

    m_open = mocker.mock_open()
    mocker.patch("builtins.open", m_open)
    mocker.patch("os.makedirs")

    download_har(har_dir_path, s3_url)

    mock_instance.get_object.assert_called_once_with(
        Bucket="test-bucket", Key="test_har.tar.gz"
    )

    expected_calls = [
        mocker.call(f"{har_dir_path}/{content['name']}", "wb") for content in contents
    ]
    m_open.assert_has_calls(expected_calls, any_order=True)
    handle = m_open()
    handle.write.assert_called()


def test_download_har_dont_write(mocker, mock_s3_client):
    contents = []
    mock_instance, prepare_tar_buffer = mock_s3_client
    tar_buffer = prepare_tar_buffer(contents)
    mock_instance.get_object.return_value = {"Body": tar_buffer}

    har_dir_path = "/tmp/fake/dir"
    s3_url = "s3://test-bucket/test_har.tar.gz"

    m_open = mocker.mock_open()
    mocker.patch("builtins.open", m_open)
    mocker.patch("os.makedirs")

    download_har(har_dir_path, s3_url)

    mock_instance.get_object.assert_called_once_with(
        Bucket="test-bucket", Key="test_har.tar.gz"
    )

    m_open.assert_not_called()


def test_example_with_known_contract_ids() -> None:
    contract_goal_id = "e2gmBRbTWoWAh8xpNAoqw"
    example = [
        example for example in get_all_examples() if example.id == contract_goal_id
    ][0]
    assert get_goal("contract") in example.goal


@pytest.mark.parametrize(
    "schema_name, expected",
    [
        ("valid_id", {"schema_": "details"}),
        ("another_valid_id", {"schema_": "more_details"}),
    ],
)
def test_get_fetch_schema_success(mocker: MockFixture, schema_name, expected):
    mocker.patch(
        "builtins.open", mock_open(read_data=json.dumps({schema_name: expected}))
    )
    assert get_fetch_schema(schema_name) == expected


@pytest.mark.parametrize(
    "schema_name",
    ["invalid_id", "nonexistent_id"],
)
def test_get_fetch_schema_failure(mocker: MockFixture, schema_name):
    mocker.patch(
        "builtins.open",
        mock_open(read_data=json.dumps({"real_id": {"schema_": "details"}})),
    )
    with pytest.raises(ValueError):
        get_fetch_schema(schema_name)


@pytest.mark.parametrize(
    "schema_name, expected",
    [("valid_id", "Complete the task"), ("another_valid_id", "Achieve the goal")],
)
def test_get_goal_success(mocker: MockFixture, schema_name, expected):
    mocker.patch(
        "builtins.open", mock_open(read_data=json.dumps({schema_name: expected}))
    )
    assert get_goal(schema_name) == expected


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
