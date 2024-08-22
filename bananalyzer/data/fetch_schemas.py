import json
from typing import Dict, Any

from bananalyzer.data.schemas import FetchId
from bananalyzer.data.examples import get_examples_path

"""
This file contains mapping of fetch_id to fetch schema to avoid duplicate schemas in examples.json
"""


def get_fetch_schema(fetch_id: FetchId) -> Dict[str, Any]:
    schemas_path = get_examples_path() / "schemas.json"
    with open(schemas_path, "r") as file:
        fetch_schemas = json.load(file)

    if fetch_id not in fetch_schemas:
        raise ValueError(f"Invalid fetch_id: {fetch_id}")

    return fetch_schemas[fetch_id]


def get_goal(fetch_id: FetchId) -> str:
    goals_path = get_examples_path() / "goals.json"
    with open(goals_path, "r") as file:
        goals = json.load(file)

    if fetch_id not in goals:
        raise ValueError(f"Invalid fetch_id: {fetch_id}")

    return goals[fetch_id]
