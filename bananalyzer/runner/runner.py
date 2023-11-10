# dynamic_test_runner.py
import os
import tempfile
from typing import IO, Awaitable, Callable, List

import pytest
from pydantic import BaseModel

from bananalyzer.data.schemas import Example

TestType = Callable[[], Awaitable[None]]


class BananalyzerTest(BaseModel):
    code: str
    example: Example


def generate_test(example: Example, headless: bool) -> BananalyzerTest:
    return BananalyzerTest(
        code=f"""
@pytest.mark.asyncio
async def test_{example.id.replace("-", "_")}() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless={headless})
        context = await browser.new_context()
        example = get_example_by_url("{example.url}")
         
        # The agent is imported into the global context prior to this call 
        result = await agent.run(context, example)
        for curr_eval in example.evals:
            assert curr_eval.eval_results(result)
""",
        example=example,
    )


def write_load_agent_module(f: IO[str], file_path: str) -> None:
    f.write(
        f"""
import importlib.util
import sys
from pathlib import Path

def load_agent_module():
    path = Path("{file_path}")
    module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, "{file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    globals()["agent"] = getattr(module, "agent")
load_agent_module()
"""
    )


def create_test_file(
    tests: List[BananalyzerTest], prefix: str, agent_file_path: str
) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, prefix=prefix, suffix=".py"
    ) as f:
        f.write("import pytest\n")
        f.write("from bananalyzer.data.examples import get_example_by_url\n")
        f.write("from playwright.async_api import async_playwright\n\n")
        f.write("global test\n")
        f.write("test = 'test'\n")
        write_load_agent_module(f, agent_file_path)

        for test_content in tests:
            f.write(f"{test_content.code}\n\n")

    return f.name


def run_tests(tests: List[BananalyzerTest], agent_file_path: str) -> int:
    """
    Create temporary test files based on intent, run them, and then delete them
    """
    intents = {test.example.type for test in tests}
    intent_separated_tests = [
        [test for test in tests if test.example.type == intent] for intent in intents
    ]
    test_file_names = [
        create_test_file(tests, f"{tests[0].example.type}_intent_", agent_file_path)
        for tests in intent_separated_tests
    ]

    try:
        return_code = pytest.main(test_file_names)
    finally:
        for test_file_name in test_file_names:
            os.unlink(test_file_name)

    return return_code
