import subprocess
from os import environ
from typing import Optional
from xml.etree import ElementTree

from bananalyzer import VERSION


# noinspection PyBroadException
def get_git_commit_sha() -> Optional[str]:
    if sha := environ.get("GITHUB_SHA", None):
        return sha

    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .strip()
            .decode("utf-8")
        )
    except Exception:
        return None


def enrich_report(report_path: str) -> None:
    tree = ElementTree.parse(report_path)
    root = tree.getroot()

    new_properties = [
        {"name": "bananalyzer_version", "value": VERSION},
    ]

    if sha := get_git_commit_sha():
        new_properties.append({"name": "git_commit_sha", "value": sha})

    for test_suite in root.findall("testsuite"):
        properties = test_suite.find("properties")
        if properties is None:
            properties = ElementTree.SubElement(test_suite, "properties")

        for prop in new_properties:
            property_element = ElementTree.SubElement(properties, "property")
            property_element.set("name", prop["name"])
            property_element.set("value", prop["value"])

    tree.write(report_path)
