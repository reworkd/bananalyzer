import urllib.parse
from typing import List, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bananalyzer.data.examples import (
    get_all_example_urls,
    get_all_examples,
    get_example_by_url,
)
from bananalyzer.data.schemas import Example, GoalType
from bananalyzer.runner.website_responder import get_website_responder

"""
Simple FastAPI server to view available data
"""

app = FastAPI(
    title="Banana-lyzer",
    description="A simple API to view the data collected by Banana-lyzer",
    version="0.0.1",
    docs_url="/api/docs",
)


class ExampleMeta(BaseModel):
    count: int
    goal_types: List[GoalType]
    examples: List[Example]


@app.get("/examples")
def fetch_all_examples() -> ExampleMeta:
    examples = get_all_examples()
    return ExampleMeta(
        count=len(examples),
        goal_types=list(set([example.type for example in examples])),
        examples=examples,
    )


@app.get("/urls")
def fetch_all_urls() -> List[str]:
    return get_all_example_urls()


@app.get("/url")
def fetch_page(url: Union[str, None] = None) -> str:
    # URL decode url
    url = urllib.parse.unquote(url or "")
    try:
        example = get_example_by_url(url)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Unable to find an example with that URL"
        )
    responder = get_website_responder(example)
    return responder.get_url(example)
