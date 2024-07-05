import asyncio
from datetime import datetime
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
    source: str,
    metadata: Dict[str, Any],
    tarsier_client: Tarsier,
    openai_client: OpenAI,
) -> None:
    for url in urls:
        example = await generate_fetch_example(
            url, schema, source, metadata, tarsier_client, openai_client
        )
        add_example_to_json(example)


async def generate_fetch_example(
    url: str,
    schema: Dict[str, Any],
    source: str,
    metadata: Dict[str, Any],
    tarsier_client: Tarsier,
    openai_client: OpenAI,
) -> Example:
    if source == "mhtml":
        example_id = await download_as_mhtml(url)
        mhtml_path = os.path.abspath(f"./static/examples/{example_id}/index.mhtml")
        url_to_annotate = f"file://{mhtml_path}"
    else:
        example_id = await download_as_har(url)
        url_to_annotate = url
    eval_expected = await llm_annotate_example(
        example_id, url_to_annotate, schema, source, tarsier_client, openai_client
    )
    eval = Eval(type="json_match", expected=eval_expected)
    example = Example(
        id=example_id,
        url=url,
        source=source,
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
    example_id: str,
    url: str,
    schema: Dict[str, Any],
    source: str,
    tarsier_client: Tarsier,
    openai_client: OpenAI,
) -> Dict[str, Any]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        if source == "har":
            har_path = os.path.abspath(f"./static/examples/{example_id}/cache/bananas.har")
            already_cached = os.path.isfile(har_path)
            if already_cached:
                await page.route_from_har(har_path, not_found="fallback")
            else:
                print("No HAR cache found for example ID {example_id}")
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


async def download_as_har(url: str) -> str:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Generate random example ID and create new directory
        example_id = str(uuid.uuid4())
        example_dir_path = f"./static/examples/{example_id}"
        os.makedirs(example_dir_path, exist_ok=True)

        # Make browser record all network responses into a HAR file
        now = datetime.now()
        timestamped_har_path = os.path.abspath(
            f"./static/examples/{example_id}/cache/bananas." + now.strftime("%s") + ".har"
        )
        await page.route_from_har(
            timestamped_har_path, not_found="fallback", update=True
        )

        await context.new_cdp_session(page)

        await page.goto(url, wait_until="networkidle")

        # Post-process captured HAR data
        har_path = os.path.abspath(f"./static/examples/{example_id}/cache/bananas.har")
        already_cached = os.path.isfile(har_path)
        har: Any = {}
        if not already_cached:
            temp_har_file_names = [
                fn
                for fn in os.listdir(example_dir_path + "/cache")
                if fn.endswith(".har")
            ]

            ## Read temporary files and extend main HAR object
            for temp_har_file_name in temp_har_file_names:
                temp_har_file_path = os.path.abspath(
                    example_dir_path + "/cache/" + temp_har_file_name
                )
                with open(temp_har_file_path) as f:
                    har_data = json.load(f)
                    if "log" in har and "entries" in har["log"]:
                        for new_entry in har_data["log"]["entries"]:
                            har["log"]["entries"].append(new_entry)
                    else:
                        har = har_data
                    f.close()
                os.remove(temp_har_file_path)

            ## Optimize
            if "log" in har and "entries" in har["log"]:
                for entry in har["log"]["entries"]:
                    if "response" in entry:
                        ## Change all "status": -1 to "status": 404
                        if (
                            "status" in entry["response"]
                            and entry["response"]["status"] == -1
                        ):
                            print(
                                "Changing entry response status",
                                entry["response"]["status"],
                                "to",
                                404,
                            )
                            entry["response"]["status"] = 404

            ## Save the file
            with open(har_path, "w") as f:
                f.seek(0)
                json.dump(har, f, indent=2)
                f.truncate()
                f.close()

            # convert_to_crlf(Path(har_path))

        return example_id


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

        # Generate random example ID and create new directory
        example_id = str(uuid.uuid4())
        example_dir_path = f"./static/examples/{example_id}"
        os.makedirs(example_dir_path, exist_ok=True)

        # Write MHTML content to the specified file
        mhtml_file_path = os.path.join(example_dir_path, "index.mhtml")
        with open(mhtml_file_path, "w") as f:
            f.write(mhtml)

        convert_to_crlf(Path(mhtml_file_path))

        return example_id


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
    source = "har"  # This can also be "mhtml"
    metadata = {
        "category": "unknown",
        "subcategory": "careers",
        "fetch_id": "job_posting",
    }
    await add_examples_to_json(
        urls, schema, source, metadata, tarsier_client, openai_client
    )


if __name__ == "__main__":
    asyncio.run(main())
