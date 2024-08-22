from bananalyzer import Example
from bananalyzer.data.schemas import Eval
from bananalyzer.runner.generator import PytestTestGenerator


def test_generate_test_with_single_eval() -> None:
    generator = PytestTestGenerator()
    example = Example(
        id="1",
        url="https://www.test.com",
        source="mhtml",
        category="test",
        subcategory="www",
        type="detail",
        evals=[Eval(type="json_match", expected={"key": "value"})],
        fetch_id="job_posting",
        goal=None,
    )
    test = generator.generate_test(example)
    assert "test_match_field" in test.code


def test_generate_test_with_multiple_evals() -> None:
    generator = PytestTestGenerator()
    example = Example(
        id="1",
        url="https://www.test.com",
        source="mhtml",
        category="test",
        subcategory="www",
        type="detail",
        evals=[
            Eval(type="json_match", expected={"key": "value"}),
            Eval(type="end_url_match", expected="https://www.test.com"),
        ],
        fetch_id="job_posting",
        goal=None,
    )
    test = generator.generate_test(example)
    assert "test_match_field" in test.code
    assert "test_end_url_match" in test.code


def test_generate_class_name_without_www() -> None:
    generator = PytestTestGenerator()
    example = Example(
        id="1",
        url="https://test.com",
        source="mhtml",
        category="test",
        subcategory="www",
        type="detail",
        evals=[],
        fetch_id="job_posting",
        goal=None,
    )
    class_name = generator._generate_class_name(example)
    assert class_name == "TestDetailTestCom_1"


def test_generate_class_name_with_www() -> None:
    generator = PytestTestGenerator()
    example = Example(
        id="1",
        url="https://www.test.com",
        source="mhtml",
        category="test",
        subcategory="www",
        type="detail",
        evals=[],
        fetch_id="job_posting",
        goal=None,
    )
    class_name = generator._generate_class_name(example)
    assert class_name == "TestDetailTestCom_1"


def test_generate_class_name_with_multiple_categorys() -> None:
    generator = PytestTestGenerator()
    example1 = Example(
        id="1",
        url="https://test.com",
        source="mhtml",
        category="test",
        subcategory="www",
        type="detail",
        evals=[],
        fetch_id="job_posting",
        goal=None,
    )
    example2 = Example(
        id="2",
        url="https://test.com",
        source="mhtml",
        category="test",
        subcategory="www",
        type="detail",
        evals=[],
        fetch_id="job_posting",
        goal=None,
    )
    class_name1 = generator._generate_class_name(example1)
    class_name2 = generator._generate_class_name(example2)
    assert class_name1 == "TestDetailTestCom_1"
    assert class_name2 == "TestDetailTestCom2_2"
