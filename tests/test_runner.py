import pytest
from _pytest.config import ExitCode

from bananalyzer import Example
from bananalyzer.runner.runner import BananalyzerTest, run_tests
from bananalyzer.schema import AgentRunnerClass, PytestArgs


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


def test_run_tests(
    runner: AgentRunnerClass, pytest_args: PytestArgs, example: Example
) -> None:
    passing_test = BananalyzerTest(
        example=example,
        code="""
def test_addition() -> None:
    assert 1 + 1 == 2
""",
    )

    exit_code, *_ = run_tests([passing_test], runner, pytest_args)
    assert exit_code == ExitCode.OK


def test_run_exception_test(
    runner: AgentRunnerClass, pytest_args: PytestArgs, example: Example
) -> None:
    exception_test = """
def test_exception() -> None:
    raise Exception("Test")
"""

    exception_test = BananalyzerTest(
        example=example,
        code=exception_test,
    )

    exit_code, *_ = run_tests([exception_test], runner, pytest_args)
    assert exit_code == ExitCode.TESTS_FAILED
