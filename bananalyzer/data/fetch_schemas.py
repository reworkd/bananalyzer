import json
from typing import Dict, Any

from bananalyzer.data.schemas import SchemaName
from bananalyzer.data.examples import get_examples_path

"""
This file maps a schema_name to a JSON schema or goal string.
"""


def get_fetch_schema(schema_name: SchemaName) -> Dict[str, Any]:
    schemas_path = get_examples_path() / "schemas.json"
    with open(schemas_path, "r") as file:
        fetch_schemas = json.load(file)

    if schema_name not in fetch_schemas:
        raise ValueError(f"Invalid schema_name: {schema_name}")

    return fetch_schemas[schema_name]


def get_goal(schema_name: SchemaName) -> str:
    goals_path = get_examples_path() / "goals.json"
    with open(goals_path, "r") as file:
        goals = json.load(file)

    if schema_name not in goals:
        raise ValueError(f"Invalid schema_name: {schema_name}")

    return goals[schema_name]
