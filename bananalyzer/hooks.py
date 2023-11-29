from typing import Any

import pytest
from _pytest.terminal import TerminalReporter
from tabulate import tabulate


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


class BananalyzerPytestPlugin:
    @pytest.hookimpl(trylast=True)
    def pytest_terminal_summary(
        self, terminalreporter: TerminalReporter, *args: Any, **kwargs: Any
    ) -> None:
        terminalreporter.section("Bananalyzer Results")

        results: dict[str, dict[str, dict[bool, int]]] = {}
        for test_result in (
            terminalreporter.stats.get("passed", [])
            + terminalreporter.stats.get("failed", [])
            + terminalreporter.stats.get("error", [])
        ):
            for key, value in test_result.user_properties:
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

        if "field" in results:
            terminalreporter.write_line("Field Results:")
            print_field_data(terminalreporter, results["field"])

        if "class" in results:
            terminalreporter.write_line("Class Results:")
            print_field_data(terminalreporter, results["class"])

        table_data = {
            "Total Tests": total_tests,
            "Tests Passed": total_passed,
            "Tests Failed": total_failed,
            "Percent Passed": f"{total_passed / total_tests * 100:.2f}%",
        }

        terminalreporter.write_line("Summary:")
        terminalreporter.write_line(tabulate(table_data.items(), tablefmt="psql"))

    # noinspection PyBroadException
    @pytest.fixture(autouse=True)
    def add_user_properties(self, record_property, request) -> None:  # type: ignore
        for key, accessor in {
            "field": lambda *_: request.node.callspec.params.get("key"),
            "class": lambda *_: request.cls.__name__,
        }.items():
            try:
                record_property(key, accessor())
            except Exception:
                pass
