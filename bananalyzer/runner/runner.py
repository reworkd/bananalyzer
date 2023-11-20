# dynamic_test_runner.py
import os
import tempfile
from typing import IO, Awaitable, Callable, Dict, List
from urllib.parse import urlparse

import pytest
from pydantic import BaseModel

from bananalyzer import AgentRunner
from bananalyzer.data.schemas import Example
from bananalyzer.schema import AgentRunnerClass, PytestArgs

TestType = Callable[[], Awaitable[None]]


class BananalyzerTest(BaseModel):
    code: str
    example: Example


class TestGenerator:
    def __init__(self) -> None:
        self._names: Dict[str, int] = {}

    def generate_test(self, example: Example, headless: bool) -> BananalyzerTest:
        return BananalyzerTest(
            code=f"""
@pytest.mark.asyncio
async def {self._generate_name(example)}() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless={headless})
        context = await browser.new_context()
        example = get_example_by_url("{example.url}")

        # The agent is imported into the global context prior to this call
        result = await agent.run(context, example)
        for curr_eval in example.evals:
            curr_eval.eval_results(p, result)
    """,
            example=example,
        )

    def _generate_name(self, example: Example) -> str:
        domain = urlparse(example.url).netloc
        domain = domain.replace(".", "_")
        if domain.startswith("www_"):
            domain = domain[4:]

        key = f"{example.type}_{domain}"
        self._names[key] = self._names.get(key, -1) + 1
        suffix = "" if not self._names[key] else f"_{self._names[key]}"
        return f"test_{key}{suffix}"


def write_load_agent_module(f: IO[str], runner: AgentRunnerClass) -> None:
    f.write(
        f"""
import importlib.util
import sys
from pathlib import Path
import pprint

def load_agent_module():
    path = Path("{runner.class_path}")
    module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    print(f"Loaded agent module", module)
    globals()["agent"] = getattr(module, '{runner.class_name}')()
    print(f"Loaded agent", agent)
load_agent_module()
"""
    )


def create_test_file(
    tests: List[BananalyzerTest], prefix: str, runner: AgentRunnerClass
) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, prefix=prefix, suffix=".py"
    ) as f:
        f.write("import pytest\n")
        f.write("from bananalyzer.data.examples import get_example_by_url\n")
        f.write("from playwright.async_api import async_playwright\n\n")
        f.write("global test\n")
        f.write("test = 'test'\n")
        write_load_agent_module(f, runner)

        for test_content in tests:
            f.write(f"{test_content.code}\n\n")

    return f.name


def run_tests(
    tests: List[BananalyzerTest], runner: AgentRunnerClass, pytest_args: PytestArgs
) -> int:
    """
    Create temporary test files based on intent, run them, and then delete them
    """
    intents = {test.example.type for test in tests}
    intent_separated_tests = [
        [test for test in tests if test.example.type == intent] for intent in intents
    ]
    test_file_names = [
        create_test_file(tests, f"{tests[0].example.type}_intent_", runner)
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
