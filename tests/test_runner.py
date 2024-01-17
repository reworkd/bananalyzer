from tempfile import NamedTemporaryFile
from typing import Union

import pytest
from _pytest.config import ExitCode

from bananalyzer import Example
from bananalyzer.hooks import BananalyzerPytestPlugin
from bananalyzer.runner.runner import BananalyzerTest, run_tests
from bananalyzer.schema import AgentRunnerClass, PytestArgs, XDistArgs


@pytest.fixture
def runner():
    return AgentRunnerClass(
        class_path="tests/test_runner.py",
        class_name="NullAgentRunner",
    )


@pytest.fixture
def pytest_args():
    return PytestArgs(
        s=False,
        n=None,
        q=False,
        xml=None,
    )


@pytest.fixture
def xdist_args():
    return XDistArgs(
        dist="no",
        n="0",
    )


@pytest.fixture
def example():
    return Example(
        id="test",
        url="https://example.com",
        subcategory="test",
        type="links",
        category="test",
        goal="links",
        source="hosted",
        evals=[],
    )


@pytest.fixture
def passing_test(example):
    return BananalyzerTest(
        example=example,
        code="""
def test_passing():
    assert True
""",
    )


@pytest.fixture
def passing_test_with_marks(example):
    return BananalyzerTest(
        example=example,
        code=f"""
import pytest
@pytest.mark.{BananalyzerPytestPlugin.MARKER_PREFIX}intent("links")
@pytest.mark.{BananalyzerPytestPlugin.MARKER_PREFIX}key("value")
def test_passing_with_marks():
    pass
""",
    )


@pytest.fixture
def failing_test(example):
    return BananalyzerTest(
        example=example,
        code="""
def test_failing():
    assert False
""",
    )


@pytest.fixture
def error_test(example):
    return BananalyzerTest(
        example=example,
        code="""
def test_erroring():
    raise Exception("Error!")
""",
    )


def test_run_tests(
    runner: AgentRunnerClass,
    pytest_args: PytestArgs,
    xdist_args: XDistArgs,
    passing_test: BananalyzerTest,
) -> None:
    exit_code = run_tests([passing_test], runner, pytest_args, xdist_args)
    assert exit_code == ExitCode.OK


def test_run_failing_test(
    runner: AgentRunnerClass,
    pytest_args: PytestArgs,
    xdist_args: XDistArgs,
    failing_test: BananalyzerTest,
) -> None:
    exit_code = run_tests([failing_test], runner, pytest_args, xdist_args)
    assert exit_code == ExitCode.TESTS_FAILED


def test_run_error_test(
    runner: AgentRunnerClass,
    pytest_args: PytestArgs,
    xdist_args: XDistArgs,
    error_test: BananalyzerTest,
) -> None:
    exit_code = run_tests([error_test], runner, pytest_args, xdist_args)
    assert exit_code == ExitCode.TESTS_FAILED


@pytest.mark.parametrize(
    "workers_count",
    [
        0,
        1,
        2,
        "auto",
    ],
)
def test_xlm_report_has_properties(
    mocker,
    runner: AgentRunnerClass,
    pytest_args: PytestArgs,
    xdist_args: XDistArgs,
    passing_test: BananalyzerTest,
    passing_test_with_marks: BananalyzerTest,
    workers_count: Union[int, str],
) -> None:
    xdist_args.n = workers_count

    mocker.patch("bananalyzer.junit.VERSION", "1.2.3")
    mocker.patch("bananalyzer.junit.get_git_commit_sha", return_value="abc123")

    with NamedTemporaryFile(suffix=".xml", prefix="test_report") as f:
        pytest_args.xml = f.name
        exit_code = run_tests(
            [passing_test_with_marks, passing_test], runner, pytest_args, xdist_args
        )

        assert exit_code == ExitCode.OK
        xml = f.read().decode("utf-8")

        # Test case level
        assert '<property name="key" value="value" />' in xml
        assert '<property name="intent" value="links" />' in xml

        # Test suite level
        assert '<property name="bananalyzer_version" value="1.2.3" />' in xml
        assert '<property name="git_commit_sha" value="abc123" />' in xml
