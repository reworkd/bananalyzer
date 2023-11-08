import asyncio
import os
from typing import List, Any

from playwright.async_api import async_playwright

from bananalyzer import examples
from bananalyzer.data.schemas import Example

"""
Test script to re-load websites and save them as MHTML files.
"""


async def save_page_as_mhtml(client: Any, page: Any, file_path: str) -> None:
    # Wait for 2 seconds
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
        client = await context.new_cdp_session(page)

        for item in examples:
            print(item.id, item.url)
            folder_path: str = f"./python/bananalyzer/data/{item.id}"
            os.makedirs(folder_path, exist_ok=True)
            file_path: str = os.path.join(folder_path, "index.mhtml")

            await page.goto(item.url)
            await save_page_as_mhtml(client, page, file_path)

        await browser.close()


if __name__ == "__main__":
    print(examples)
    asyncio.run(setup_and_save(examples))
