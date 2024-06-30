from typing import Dict
from urllib.parse import urlparse

from bananalyzer import Example
from bananalyzer.data.schemas import Eval
from bananalyzer.runner.runner import BananalyzerTest
from bananalyzer.schema import MARKER_PREFIX


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
    async def result(self, page, agent_constructor):
        agent = agent_constructor()
        yield await agent.run(page, self.example)

    {"".join(self._generate_eval_test(eval_, i, {
                "category": example.category,
                "subcategory": example.subcategory,
                "type": example.type,
            }) for i, eval_ in enumerate(example.evals))}
""",
            example=example,
        )

    @staticmethod
    def _generate_eval_test(eval_: Eval, i: int, attrs: dict[str, str]) -> str:
        marks = "\n    ".join(
            f"@pytest.mark.{MARKER_PREFIX}{k}('{v}')" for k, v in attrs.items()
        )

        if eval_.type == "json_match" and isinstance(eval_.expected, dict):
            return f"""
    {marks}
    @pytest.mark.parametrize("key", {list(eval_.expected.keys())})
    async def test_match_field(self, key, result) -> None:
        self.example.evals[{i}].eval_results(None, result, field=key)

"""
        return f"""
    {marks}
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
        return f"Test{key}{suffix}_{example.id.replace('-', '_')}"
