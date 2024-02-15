import asyncio
import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI
from playwright.async_api import async_playwright
from tarsier import GoogleVisionOCRService, Tarsier

from bananalyzer.data.examples import convert_to_crlf
from bananalyzer.data.fetch_schemas import get_fetch_schema
from bananalyzer.data.schemas import Eval, Example


async def add_examples_to_json(
    urls: List[str],
    schema: Dict[str, Any],
    metadata: Dict[str, Any],
    tarsier_client: Tarsier,
    openai_client: OpenAI,
) -> None:
    for url in urls:
        example = await generate_fetch_example(
            url, schema, metadata, tarsier_client, openai_client
        )
        add_example_to_json(example)


async def generate_fetch_example(
    url: str,
    schema: Dict[str, Any],
    metadata: Dict[str, Any],
    tarsier_client: Tarsier,
    openai_client: OpenAI,
) -> Example:
    example_id = await download_as_mhtml(url)
    mhtml_path = os.path.abspath(f"./static/{example_id}/index.mhtml")
    file_url = f"file://{mhtml_path}"
    eval_expected = await llm_annotate_example(
        file_url, schema, tarsier_client, openai_client
    )
    eval = Eval(type="json_match", expected=eval_expected)
    example = Example(
        id=example_id,
        url=url,
        source="mhtml",
        category=metadata["category"],
        subcategory=metadata["subcategory"],
        type="fetch",
        fetch_id=metadata["fetch_id"],
        evals=[eval],
        goal=None,
    )
    if hasattr(example, "goal"):
        delattr(example, "goal")
    return example


async def llm_annotate_example(
    url: str, schema: Dict[str, Any], tarsier_client: Tarsier, openai_client: OpenAI
) -> Dict[str, Any]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")
        page_text, _ = await tarsier_client.page_to_text(page, False)

    prompt = f"""Here's an OCR'd screenshot of the details page for a listing on a website.
{page_text}

Here is the schema we want to map information from the details page into. If an attribute in this schema doesn't have corresponding information on the details page, do set that attribute as null in your output. If there is no corresponding information on the page at all, return an empty JSON.
```json
{schema}
```

For each attribute in the schema, find information on the details page that would serve as its value and return it as part of a JSON object (formatted as ```json ...``` with double quotes for property names) mapping the attribute key to the information. For attributes that are a list of objects, remember to provide well-formed JSON for each object in the list."""

    completion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    output = completion.choices[0].message.content
    assert isinstance(output, str)

    json_start = output.find("```json")
    if json_start == -1:
        details = {}
    else:
        json_start += len("```json")
        json_end = output.find("```", json_start)
        json_output = output[json_start:json_end].strip()
        try:
            details = json.loads(json_output)
        except json.JSONDecodeError:
            details = {}

    return details


async def download_as_mhtml(url: str) -> str:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        client = await context.new_cdp_session(page)

        await page.goto(url, wait_until="networkidle")

        # Capture page content as MHTML
        result = await client.send("Page.captureSnapshot", {"format": "mhtml"})
        mhtml = result["data"]

        # Write MHTML content to the specified file
        id = str(uuid.uuid4())
        folder_path = f"./static/{id}"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "index.mhtml")
        with open(file_path, "w") as f:
            f.write(mhtml)

        convert_to_crlf(Path(file_path))

        return id


def add_example_to_json(example: Example) -> None:
    json_file_path = "./static/examples.json"
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    data.append(example.model_dump())

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write("\n")


async def main() -> None:
    openai_client = OpenAI()
    ocr_service = GoogleVisionOCRService({})
    tarsier_client = Tarsier(ocr_service)

    urls: List[str] = []
    fetch_schema = get_fetch_schema("job_posting")
    if not isinstance(fetch_schema, dict):
        schema = fetch_schema.model_fields
    else:
        schema = fetch_schema
    metadata = {
        "category": "unknown",
        "subcategory": "careers",
        "fetch_id": "job_posting",
    }
    await add_examples_to_json(urls, schema, metadata, tarsier_client, openai_client)


if __name__ == "__main__":
    asyncio.run(main())
