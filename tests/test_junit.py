import os

from bananalyzer.junit import get_git_commit_sha


def test_get_git_commit_sha():
    x = get_git_commit_sha()
    assert isinstance(x, str)


def test_github_commit_sha():
    os.environ["GITHUB_SHA"] = "abc123"
    x = get_git_commit_sha()

    assert x == "abc123"
    del os.environ["GITHUB_SHA"]
