import asyncio
import json
import os
from typing import Any, List

from playwright.async_api import async_playwright

from bananalyzer.data.examples import get_all_examples
from bananalyzer.data.schemas import Example

"""
Test script to re-load websites and create HAR cache files.
"""

async def refine_har_file(har_path: str) -> None:
    if os.path.isfile(har_path):
        har = {}

        ## Read and parse existing HAR file
        with open(har_path) as f:
            har = json.load(f)
            f.close()

        ## Optimize
        if "log" in har and "entries" in har["log"]:
            for entry in har["log"]["entries"]:
                if "response" in entry:
                    ## Change all "status": -1 to "status": 404
                    if "status" in entry["response"] and entry["response"]["status"] == -1:
                        print("Changing entry response status", entry["response"]["status"], "to", 404)
                        entry["response"]["status"] = 404

        ## Save the file
        with open(har_path, "w") as f:
            f.seek(0)
            json.dump(har, f, indent=2)
            f.truncate()
            f.close()

async def run_examples_and_create_cache(examples: List[Example]) -> None:
    async with async_playwright() as p:
        # Filter
        examples = [e for e in examples if e.source == "har"]

        for i, item in enumerate(examples):
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                page.set_default_timeout(100000)
                client = await context.new_cdp_session(page)

                print(f"[{i + 1}/{len(examples)}]", item.id, item.url)

                folder_path: str = f"examples/{item.id}"
                folder_path_abs: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_path)
                os.makedirs(folder_path_abs, exist_ok=True)
                file_path: str = os.path.join(folder_path_abs, "bananas.har")

                await page.route_from_har(file_path, not_found="fallback", update=True, update_content="embed")
                await page.goto(item.url)
                # TODO: crawl the site using agent

                await context.close()
                await browser.close()
                await refine_har_file(file_path)
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    examples = get_all_examples()
    asyncio.run(run_examples_and_create_cache(examples))
