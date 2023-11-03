import urllib.parse
from typing import Union, List

from fastapi import FastAPI, HTTPException

from bananalyzer.data.examples import get_all_example_urls, get_example_by_url
from bananalyzer.server.website_responder import get_website_responder

"""
Simple FastAPI server to view available data
"""

app = FastAPI()


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
    return responder.get_url(url)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
