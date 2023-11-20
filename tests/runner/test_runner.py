"""
NOTE: It appears that pytest.main() is not working as expected when run inside a pytest test.
Because of this, the following tests are commented out.
"""
# from _pytest.config import ExitCode
#
# from bananalyzer.runner.runner import run_tests
#
# def test_run_tests() -> None:
#     passing_test = """
# def test_addition() -> None:
#     assert 1 + 1 == 2
# """
#
#     exit_code = run_tests([passing_test])
#     assert exit_code == ExitCode.OK
#
#
# def test_run_exception_test() -> None:
#     exception_test = """
# def test_exception() -> None:
#     raise Exception("Test")
# """
#
#     exit_code = run_tests([exception_test])
#     assert exit_code == ExitCode.TESTS_FAILED
