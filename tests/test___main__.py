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


def test_report_path():
    sys.argv = ["bananalyzer", ".", "--headless", "--junitxml", "report.xml"]
    args = parse_args()
    assert args.path == "."
    assert args.headless is True
    assert args.pytest_args.xml == "report.xml"
