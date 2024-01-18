from typing import Any, Callable

import pytest
import xdist
from _pytest.config import Config
from _pytest.main import Session
from _pytest.nodes import Node
from _pytest.python import Function
from _pytest.terminal import TerminalReporter
from tabulate import tabulate

RecordProperty = Callable[[str, object], None]


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: Config) -> None:
    plugin = BananalyzerPytestPlugin()
    config.pluginmanager.register(plugin)


class BananalyzerPytestPlugin:
    """
    This plugin is responsible for collecting and marking properties of each test
    based on the markers that are applied to it. It also prints the results of each
    test to the terminal after all tests have been executed.

    Since we are using xdist, load this plugin through a conftest.py file so that
    it can be properly registered on each worker node.

    Dynamically imported in bananalyzer/runner/runner.py
    """

    MARKER_PREFIX = "bananalyzer_"

    def __init__(self) -> None:
        self.marks: dict[str, dict[str, str]] = {}
        self.record_property: RecordProperty = lambda x, y: None

    @pytest.hookimpl(trylast=True)
    def pytest_terminal_summary(
        self, terminalreporter: TerminalReporter, *args: Any, **kwargs: Any
    ) -> None:
        """
        This hook is called after all tests have been executed. We use it to print
        the results of each test. When using xdist this hook is only called on the
        master node.
        """

        terminalreporter.section("Bananalyzer Results")

        results: dict[str, dict[str, dict[bool, int]]] = {}
        for test_result in (
            terminalreporter.stats.get("passed", [])
            + terminalreporter.stats.get("failed", [])
            + terminalreporter.stats.get("error", [])
        ):
            for key, value in self.marks.get(test_result.nodeid, {}).items():
                result_property = results.setdefault(key, {})
                result_property_value = result_property.setdefault(value, {})
                result_property_value[test_result.passed] = (
                    result_property_value.get(test_result.passed, 0) + 1
                )

        total_passed = len(terminalreporter.stats.get("passed", []))
        total_failed = len(terminalreporter.stats.get("failed", [])) + len(
            terminalreporter.stats.get("error", [])
        )
        total_tests = total_passed + total_failed

        for k, v in results.items():
            terminalreporter.write_line(f"{k.capitalize()} Results:")
            self.print_field_data(terminalreporter, v)

        table_data = {
            "Total Tests": total_tests,
            "Tests Passed": total_passed,
            "Tests Failed": total_failed,
            "Percent Passed": f"{total_passed / total_tests * 100:.2f}%",
        }

        terminalreporter.write_line("Summary:")
        terminalreporter.write_line(tabulate(table_data.items(), tablefmt="psql"))

    @pytest.fixture(autouse=True)
    def add_user_properties(self, record_property: RecordProperty) -> None:
        self.record_property = record_property

    # noinspection PyBroadException
    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_call(self, item: Function) -> None:
        """
        This hook is called prior to test execution. We use it to record the marks
        associated with each test.
        """

        def record(k: str, value: str) -> None:
            self.marks.setdefault(item.nodeid, {})[k] = value
            self.record_property(k, value)

        for key, accessor in {
            "class": lambda *_: item.parent.name,  # type: ignore
            "field": lambda *_: item.callspec.params.get("key"),
        }.items():
            try:
                record(key, accessor())  # type: ignore
            except Exception:
                pass

        for mark in [
            mark
            for mark in item.iter_markers()
            if mark.name.startswith(self.MARKER_PREFIX) and len(mark.args) == 1
        ]:
            record(mark.name[len(self.MARKER_PREFIX) :], mark.args[0])

    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionstart(self, session: Session) -> None:
        """
        If using xdist, we need to emit the marks from each worker to the master. This
        hook can be called on both the worker and master nodes.
        """
        if xdist.is_xdist_worker(session):
            session.config.workeroutput["marks"] = self.marks  # type: ignore

    @pytest.hookimpl(trylast=True)
    def pytest_testnodedown(self, node: Node, *_: Any) -> None:
        """
        If using xdist, we need to collect the marks from each worker. This hook is
        called on the master node only.
        """
        if "marks" in node.workeroutput:  # type: ignore
            node_stats = node.workeroutput["marks"]  # type: ignore
            self.marks.update(node_stats)

    @staticmethod
    def print_field_data(
        terminalreporter: TerminalReporter, results: dict[str, dict[bool, int]]
    ) -> None:
        headers = "Group", "Passed", "Failed", "Correct %", "Perfect"

        table_data = []
        total_passed = 0
        total_failed = 0
        perfect_count = 0

        for field, values in results.items():
            passed = values.get(True, 0)
            failed = values.get(False, 0)
            total_passed += passed
            total_failed += failed
            is_perfect = failed == 0
            perfect_count += int(is_perfect)
            percentage = (
                f"{passed / (passed + failed) * 100:.2f}%"
                if (passed + failed) > 0
                else "N/A"
            )
            perfect = is_perfect and "✅" or "❌"
            table_data.append([field, passed, failed, percentage, perfect])

        table_data.sort(key=lambda row: row[3], reverse=True)  # type: ignore

        # Calculate the percentage for the total row
        total_percentage = (
            f"{total_passed / (total_passed + total_failed) * 100:.2f}%"
            if (total_passed + total_failed) > 0
            else "N/A"
        )
        perfect_percentage = (
            f"{perfect_count / len(results) * 100:.2f}%" if results else "N/A"
        )

        # Add a totals row
        table_data.append(["-" * len(header) for header in headers])
        table_data.append(
            ["Total", total_passed, total_failed, total_percentage, perfect_percentage]
        )

        # Create a table using tabulate
        table = tabulate(table_data, headers=headers, tablefmt="psql")

        # Print the table
        terminalreporter.write_line(table)
        terminalreporter.write_line("\n")
