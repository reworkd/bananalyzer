# dynamic_test_runner.py
import asyncio
import os
import tempfile
from typing import IO, Awaitable, Callable, Dict, List
from urllib.parse import urlparse

import pytest
from pydantic import BaseModel

from bananalyzer import AgentRunner
from bananalyzer.data.schemas import Example, Eval
from bananalyzer.schema import AgentRunnerClass, PytestArgs

TestType = Callable[[], Awaitable[None]]


class BananalyzerTest(BaseModel):
    code: str
    example: Example


class TestGenerator:
    def __init__(self) -> None:
        self._names: Dict[str, int] = {}
        self._classnames: Dict[str, int] = {}

    def generate_test(self, example: Example) -> BananalyzerTest:
        return BananalyzerTest(
            code=f"""
@pytest.mark.asyncio
class {self._generate_class_name(example)}:

    @classmethod
    def setup_class(cls):
        cls.example = get_example_by_url("{example.url}")


    @pytest_asyncio.fixture(scope="class")
    async def result(self, context, agent):
        yield await agent.run(context, self.example)

    {"".join(self._generate_eval_test(eval_, i) for i, eval_ in enumerate(example.evals))}
""",
            example=example,
        )

    def _generate_eval_test(self, eval_: Eval, i: int) -> str:
        if eval_.type == "json_match" and isinstance(eval_.expected, dict):
            return f"""
    @pytest.mark.parametrize("key", {list(eval_.expected.keys())})
    async def test_match_field(self, key, result) -> None:
        assert self.example.evals[{i}].expected[key] == result[key]

"""
        return f"""
    async def test_{eval_.type}(self, result) -> None:
        self.example.evals[{i}].eval_results(None, result)

"""

    def _generate_name(self, example: Example) -> str:
        domain = urlparse(example.url).netloc
        domain = domain.replace(".", "_")
        if domain.startswith("www_"):
            domain = domain[4:]

        key = f"{example.type}_{domain}"
        self._names[key] = self._names.get(key, -1) + 1
        suffix = "" if not self._names[key] else f"_{self._names[key]}"
        return f"test_{key}{suffix}"

    def _generate_class_name(self, example: Example) -> str:
        domain = urlparse(example.url).netloc
        domain = domain.replace(".", "_")
        if domain.startswith("www_"):
            domain = domain[4:]

        domain = domain.split("_")
        domain = "".join([part.capitalize() for part in domain])

        key = f"{example.type.capitalize()}{domain}"
        self._classnames[key] = self._classnames.get(key, -1) + 1
        suffix = "" if not self._classnames[key] else f"{self._classnames[key]}"
        return f"Test{key}{suffix}"


def create_test_file(
    tests: List[BananalyzerTest], prefix: str, runner: AgentRunnerClass, headless: bool
) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w+",
        delete=False,
        prefix=prefix,
        suffix=".py",
        dir=os.path.dirname(os.getcwd() + "/.bananalyzer_cache"),
    ) as f:
        # noinspection PyUnresolvedReferences
        f.write(
            f"""
import pytest
import pytest_asyncio
import asyncio

from bananalyzer.data.examples import get_example_by_url
from playwright.async_api import async_playwright


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def agent():
    import importlib.util
    import sys
    from pathlib import Path
    import pprint


    path = Path("{runner.class_path}")
    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    print(f"Loaded agent module", module)

    agent_ = getattr(module, '{runner.class_name}')()
    yield agent_


@pytest_asyncio.fixture(scope="session")
async def context():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless={headless})
        context = await browser.new_context()
        yield context
        await browser.close()

"""
        )
        for test_content in tests:
            f.write(f"{test_content.code}\n\n")

    return f.name


def run_tests(
    tests: List[BananalyzerTest],
    runner: AgentRunnerClass,
    pytest_args: PytestArgs,
    headless: bool,
) -> int:
    """
    Create temporary test files based on intent, run them, and then delete them
    """
    intents = {test.example.type for test in tests}
    intent_separated_tests = [
        [test for test in tests if test.example.type == intent] for intent in intents
    ]
    test_file_names = [
        create_test_file(tests, f"{tests[0].example.type}_intent_", runner, headless)
        for tests in intent_separated_tests
    ]

    try:
        args = (
            test_file_names
            + (["-s"] if pytest_args.s else [])
            + ([f"-n {pytest_args.n}"] if pytest_args.n else [])
            + ["-v"]
        )
        return_code = pytest.main(args)
    finally:
        for test_file_name in test_file_names:
            os.unlink(test_file_name)

    return return_code
