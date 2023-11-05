# dynamic_test_runner.py
from typing import Callable, Awaitable, List

import pytest

from bananalyzer.data.schemas import Example

Test = Callable[[], Awaitable[None]]


def generate_test(example: Example) -> str:
    return f"""
@pytest.mark.asyncio
async def test_{example.id.replace("-", "_")}() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        agent = AgentWrapper()
        example = get_example_by_url("{example.url}") 
        result = agent.run(context, example)
        for curr_eval in example.evals:
            assert curr_eval.eval_results(result)
"""


def run_tests(tests: List[str]) -> int:
    """
    Create temporary test file and run it
    """
    test_file_name = "dynamic_tests.py"
    with open(test_file_name, "w") as f:
        # Write necessary imports at the top of the file
        f.write("import pytest\n")
        f.write("from bananalyzer.data.examples import get_example_by_url\n")
        f.write("from bananalyzer.runner.agent_runner import AgentWrapper\n")
        f.write("from playwright.async_api import async_playwright\n\n")

        # Write each test to the file
        for test in tests:
            f.write(f"{test}\n\n")

    # Now that all tests are written to the file, run them with pytest
    return pytest.main([test_file_name])
