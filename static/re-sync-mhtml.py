import asyncio
import os
from typing import Any, List

from playwright.async_api import async_playwright

from bananalyzer.data.example_fetching import get_all_examples
from bananalyzer.data.example_schemas import Example

"""
Test script to re-load websites and save them as MHTML files.
"""


async def save_page_as_mhtml(client: Any, page: Any, file_path: str) -> None:
    await asyncio.sleep(3)

    # Check if the file exists before trying to delete it
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the page as MHTML
    result = await client.send("Page.captureSnapshot", {"format": "mhtml"})
    mhtml = result["data"]
    with open(file_path, "w") as file:
        file.write(mhtml)


async def setup_and_save(examples: List[Example]) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(100000)
        client = await context.new_cdp_session(page)

        for item in examples:
            try:
                print(item.id, item.url)
                folder_path: str = f"./python/bananalyzer/data/{item.id}"
                os.makedirs(folder_path, exist_ok=True)
                file_path: str = os.path.join(folder_path, "index.mhtml")

                await page.goto(item.url)
                await save_page_as_mhtml(client, page, file_path)
            except Exception as e:
                print(e)
                continue

        await browser.close()


if __name__ == "__main__":
    examples = get_all_examples()
    print(examples)
    asyncio.run(setup_and_save(examples))
