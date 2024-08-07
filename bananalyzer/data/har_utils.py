import asyncio
from typing import Any, Awaitable, Callable, Optional
from datetime import datetime
import shutil
import json
import re
import os
from urllib.parse import urlparse
import nanoid
from playwright.async_api import async_playwright, Page, ElementHandle

# from playwright.sync_api import sync_playwright, Page

import harambe
from harambe.observer import InMemoryObserver

from bananalyzer.data.schemas import Example


async def serve_multipage_example(base_url: str, example_dir_path: str) -> None:
    har_path = os.path.abspath(f"{example_dir_path}/index.har")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(service_workers="block")

        await context.route_from_har(har_path, not_found="abort", update=False)

        page = await context.new_page()
        await context.new_cdp_session(page)

        await page.goto(base_url)

        await asyncio.sleep(30)


def fuse_hars(base_har_path: str, target_har_paths: list[str]) -> None:
    """
    Takes a base HAR file path and a list of target HAR file paths, reads their content, and combines the target HARs into the base HAR.
    Additionally, copies all associated resources from the target HAR directories to the base HAR directory.

    Args:
        base_har_path (str): Path to the base HAR file to be updated.
        target_har_paths (list[str]): List of paths to HAR files to be combined into the base HAR.
    """
    with open(base_har_path, "r") as file:
        base_har_data = json.load(file)

    base_har_dir = os.path.dirname(base_har_path)

    for har_path in target_har_paths:
        with open(har_path, "r") as file:
            har_data = json.load(file)

        target_har_dir = os.path.dirname(har_path)
        target_dir_name = os.path.basename(target_har_dir)
        filename_mapping = {}

        for item in os.listdir(target_har_dir):
            source_path = os.path.join(target_har_dir, item)
            if not source_path.endswith(".har"):
                file_extension = os.path.splitext(item)[1]
                new_filename = (
                    f"{os.path.splitext(item)[0]}_{target_dir_name}{file_extension}"
                )
                destination_path = os.path.join(base_har_dir, new_filename)
                shutil.copy2(source_path, destination_path)
                filename_mapping[item] = new_filename

        # Update references to the copied files in the HAR (request.postData._file, response.content._file)
        for entry in har_data["log"]["entries"]:
            if (
                "request" in entry
                and "postData" in entry["request"]
                and "_file" in entry["request"]["postData"]
            ):
                old_file = entry["request"]["postData"]["_file"]
                if old_file in filename_mapping:
                    entry["request"]["postData"]["_file"] = filename_mapping[old_file]

            if (
                "response" in entry
                and "content" in entry["response"]
                and "_file" in entry["response"]["content"]
            ):
                old_file = entry["response"]["content"]["_file"]
                if old_file in filename_mapping:
                    entry["response"]["content"]["_file"] = filename_mapping[old_file]

        # # NOTE: switch to slow but general recursive function if needed
        # def update_file_references(entry, filename_mapping):
        #     if isinstance(entry, dict):
        #         for key, value in entry.items():
        #             if key == "_file" and value in filename_mapping:
        #                 entry[key] = filename_mapping[value]
        #             elif isinstance(value, dict) or isinstance(value, list):
        #                 update_file_references(value, filename_mapping)

        # for entry in har_data["log"]["entries"]:
        #     update_file_references(entry, filename_mapping)

        base_har_data["log"]["entries"].extend(har_data["log"].get("entries", []))

    with open(base_har_path, "w") as file:
        json.dump(base_har_data, file, indent=4)

    for har_path in target_har_paths:
        shutil.rmtree(os.path.dirname(har_path))


def create_nano_id() -> str:
    disallowed = ["-", "_"]
    nano_id = nanoid.generate()
    while any([item in nano_id for item in disallowed]):
        nano_id = nanoid.generate()
    return nano_id


async def create_har(
    url: str, example_dir_path: str, scraper: Callable
) -> InMemoryObserver:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(service_workers="block")
        page = await context.new_page()

        os.makedirs(example_dir_path, exist_ok=True)
        har_path = os.path.abspath(f"{example_dir_path}/index.har")

        await page.route_from_har(har_path, update=True)
        await page.goto(url, wait_until="networkidle")

        observer = InMemoryObserver()
        sdk = harambe.SDK(page, observer=observer)
        sdk._scraper = scraper
        await scraper(sdk, url, {})

        await context.close()

    return observer


async def create_end2end_examples(
    base_url: str, metadata: dict, listing_scraper: Callable, detail_scraper: Callable
):
    domain = urlparse(base_url).netloc.replace("www.", "").replace(".", "_")

    observer = await create_har(base_url, f"./static/{domain}", listing_scraper)
    enqueued_urls = [url for url, context, options in observer.urls]

    examples = [
        Example(
            id=create_nano_id(),
            url=base_url,
            resource_path=f"./static/{domain}/index.har",
            source="har",
            category=metadata["category"],
            subcategory=metadata["subcategory"],
            type="links",
            goal=metadata["goal"],
            evals=[{"type": "json_match", "expected": enqueued_urls}],
        )
    ]

    enqueued_urls = enqueued_urls[:3]

    for i, url in enumerate(enqueued_urls):
        observer = await create_har(url, f"./static/{domain}_detail{i}", detail_scraper)
        observer_data = observer.data[0]
        observer_data.pop("__url")

        examples.append(
            Example(
                id=create_nano_id(),
                url=url,
                resource_path=f"./static/{domain}/index.har",
                source="har",
                category=metadata["category"],
                subcategory=metadata["subcategory"],
                type="fetch",
                fetch_id=metadata["fetch_id"],
                evals=[{"type": "json_match", "expected": observer_data}],
            )
        )

    fuse_hars(
        f"./static/{domain}/index.har",
        [f"./static/{domain}_detail{i}/index.har" for i in range(len(enqueued_urls))],
    )

    with open(f"./static/examples.json", "r+") as file:
        current_data = json.load(file)
        current_data.extend([example.model_dump(exclude_unset=True, exclude_none=True) for example in examples])
        file.seek(0)
        file.truncate()
        json.dump(current_data, file, indent=2)



async def scrape_listing(
    sdk: harambe.SDK, current_url: str, *args: Any, **kwargs: Any
) -> None:
    page: Page = sdk.page
    # await page.goto(current_url)
    await page.wait_for_timeout(5000)

    # previous_height = await page.evaluate('document.body.scrollHeight')
    # while True:
    #     await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    #     await asyncio.sleep(3)  # Wait for new data to load
    #     current_height = await page.evaluate('document.body.scrollHeight')
    #     if current_height == previous_height:
    #         break  # No more new data
    #     previous_height = current_height
    #     await page.wait_for_selector('.product-card__body > figure > .product-card__link-overlay', timeout=15000)

    faculty_rows = await page.query_selector_all(
        ".product-card__body > figure > .product-card__link-overlay"
    )
    for row in faculty_rows:
        next_url = await row.get_attribute("href")
        if next_url:
            await sdk.enqueue(next_url)


async def scrape_detail(
    sdk: harambe.SDK, current_url: str, *args: Any, **kwargs: Any
) -> None:
    page: Page = sdk.page
    await page.wait_for_timeout(2000)
    # await page.wait_for_selector('#pdp_product_title')
    await page.wait_for_load_state('networkidle')
    
    product_name_element = await page.query_selector("#pdp_product_title")
    product_subname_element = await page.query_selector("#pdp_product_subtitle")
    product_name = await product_name_element.inner_text() if product_name_element else None
    product_subname = await product_subname_element.inner_text() if product_subname_element else None
    if product_name and product_subname:
        product_name = f"{product_name} - {product_subname}"
    elif product_subname:
        product_name = product_subname

    categories_elements = await page.query_selector_all('h2[data-test="product-sub-title"]')
    categories = [await x.inner_text() for x in categories_elements if x]
    categories = list(set(categories))

    product_description_button = await page.query_selector(".btn-lg.readMoreBtn")
    if product_description_button:
        await product_description_button.click()
        await page.wait_for_timeout(1000)
        await page.wait_for_selector('.pi-pdpmainbody')
        product_description_element = await page.query_selector(".pi-pdpmainbody")
        close_button = await page.query_selector(".dialog__close-btn.close-btn")
        await close_button.click()
        await page.wait_for_timeout(1000)
    else:
        product_description_element = await page.query_selector("#product-description-container")
    product_description = await product_description_element.text_content() if product_description_element else None

    price_elements = await page.query_selector_all("#price-container > span")
    if len(price_elements) == 2:
        discounted_price_element, price_element = price_elements
    else:
        price_element = price_elements[0]
        discounted_price_element = None
    price = await price_element.text_content() if price_element else None
    price = re.sub(r'[^0-9.]', '', price) if price else None
    discounted_price = await discounted_price_element.text_content() if discounted_price_element else None
    discounted_price = re.sub(r'[^0-9.]', '', discounted_price) if discounted_price else None

    size_elements = await page.query_selector_all("#size-selector > fieldset > div > div")
    size = [await x.inner_text() for x in size_elements if x]
    size = [x.strip() for x in size if x]

    color_elements = await page.query_selector_all("#colorway-picker-container > a > img")
    color = [await x.get_attribute("alt") for x in color_elements if x]
    color = [x.strip() for x in color if x]

    images_elements = await page.query_selector_all('[data-testid="ThumbnailListContainer"] > div > label > img')
    images = [await x.get_attribute("src") for x in images_elements if x]

    shipping_details_element = await page.query_selector('#shippingPickup')
    shipping_details = await shipping_details_element.text_content() if shipping_details_element else None

    # return_policy_element = await page.query_selector('details[data-test="shippingAccordionClick"]')
    # return_policy = await return_policy_element.text_content() if return_policy_element else None

    await sdk.save_data(
        {
            "product_id": current_url.rsplit("/")[-1],
            "product_name": product_name,
            "categories": categories,
            "product_description": product_description,
            "price": price,
            "discounted_price": discounted_price,
            "size": size,
            "color": color,
            "images": images,
            "availability": None,
            "shipping_details": shipping_details,
            "return_policy": None,
            "tags": categories,
        }
    )


if __name__ == "__main__":
    # run listing scraper
    #    output expected list of enqueued urls
    #    save har
    # grab first 3 urls from enqueued urls
    #    run detail scraper on each one
    #    output expected detail data for each one
    #    save har for each one
    # fuse hars and save to static/
    #    delete old har folders
    # write expected 1 listing & 3 detail examples to examples.json
    #    include subpage path for detail examples. no! just use url attribute

    base_url = "https://www.nike.com/w/clothing-6ymx6"
    metadata = {
        "category": "clothing",
        "subcategory": "commerce",
        "fetch_id": "manufacturing_commerce",
        "goal": "Extract the product information from the given URL of an e-commerce site. You do not have to navigate to other pages as the URL contains all the necessary product details. Ensure you paginate if the site has multiple pages of products. Pagination controls can look like a series of numbers in a row at the bottom of product lists. Do not click random buttons. If the data is not on the page, then leave it as null. The information for a single product should be clustered together.",
    }

    asyncio.run(
        create_end2end_examples(base_url, metadata, scrape_listing, scrape_detail)
    )

    # asyncio.run(serve_multipage_example(base_url, "./static/{}"))
