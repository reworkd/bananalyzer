import sys

import pytest

from bananalyzer.__main__ import parse_args


def test_parse_args_with_no_arguments():
    sys.argv = ["bananalyzer"]
    with pytest.raises(SystemExit):
        parse_args()


def test_parse_without_path():
    sys.argv = ["bananalyzer", "--headless"]
    with pytest.raises(SystemExit):
        parse_args()


def test_parse_with_path():
    sys.argv = ["bananalyzer", "path/to/file.py", "--headless"]
    args = parse_args()
    assert args.path == "path/to/file.py"
    assert args.headless is True


def test_download_only():
    sys.argv = ["bananalyzer", "--download"]
    args = parse_args()
    assert args.path == "DOWNLOAD_ONLY"


@pytest.mark.parametrize(
    "id_input, expected",
    [
        (
            "a4c8292a-079c-4e49-bca1-cf7c9da205ec",
            ["a4c8292a-079c-4e49-bca1-cf7c9da205ec"],
        ),
        (
            "a4c8292a_079c_4e49_bca1_cf7c9da205ec",
            ["a4c8292a-079c-4e49-bca1-cf7c9da205ec"],
        ),
        ("a4c8292a-079c,bca1-cf7c9da205ec", ["a4c8292a-079c", "bca1-cf7c9da205ec"]),
        ("a4c8292a_079c,bca1_cf7c9da205ec", ["a4c8292a-079c", "bca1-cf7c9da205ec"]),
    ],
)
def test_parse_with_id(id_input, expected):
    sys.argv = ["bananalyzer", "path/to/file.py", "--id", id_input]
    args = parse_args()
    print(args.id)
    assert args.id == expected


def test_report_path():
    sys.argv = ["bananalyzer", ".", "--headless", "--junitxml", "report.xml"]
    args = parse_args()
    assert args.path == "."
    assert args.headless is True
    assert args.pytest_args.xml == "report.xml"
