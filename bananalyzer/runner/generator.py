from typing import Dict
from urllib.parse import urlparse

from bananalyzer import Example
from bananalyzer.data.schemas import Eval
from bananalyzer.runner.runner import BananalyzerTest


class PytestTestGenerator:
    def __init__(self) -> None:
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
    async def result(self, page, agent):
        yield await agent.run(page, self.example)

    {"".join(self._generate_eval_test(eval_, i) for i, eval_ in enumerate(example.evals))}
""",
            example=example,
        )

    def _generate_eval_test(self, eval_: Eval, i: int) -> str:
        if eval_.type == "json_match" and isinstance(eval_.expected, dict):
            return f"""
    @pytest.mark.parametrize("key", {list(eval_.expected.keys())})
    async def test_match_field(self, key, result) -> None:
        self.example.evals[{i}].eval_results(None, result, field=key)

"""
        return f"""
    async def test_{eval_.type}(self, page, result) -> None:
        self.example.evals[{i}].eval_results(page, result)

"""

    def _generate_class_name(self, example: Example) -> str:
        domain = urlparse(example.url).netloc
        domain = domain.replace(".", "_")
        domain = domain.replace("-", "_")
        if domain.startswith("www_"):
            domain = domain[4:]

        domain = "".join([part.capitalize() for part in domain.split("_")])

        key = f"{example.type.capitalize()}{domain}"
        self._classnames[key] = self._classnames.get(key, -1) + 1
        suffix = "" if not self._classnames[key] else f"{self._classnames[key] + 1}"
        return f"Test{key}{suffix}"
