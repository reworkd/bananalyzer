from bananalyzer.data.schemas import JSONEval


def test_json_eval() -> None:
    json = {"one": "one", "two": "two"}

    eval = JSONEval(expected=json)

    assert eval.eval_results(json)
    assert eval.eval_results({"two": "two", "one": "one"})
    assert not eval.eval_results({"test": "test"})
