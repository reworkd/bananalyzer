import boto3
import harambe
import json
import nanoid
import os
import shutil
import tarfile
from harambe.contrib.playwright.impl import PlaywrightElementHandle
from harambe.contrib.types import AbstractPage
from harambe.observer import InMemoryObserver
from io import BytesIO
from playwright.async_api import ElementHandle, Page, async_playwright
from typing import Any, Optional, cast
from urllib.parse import urlparse

from bananalyzer.data.schemas import Example

"""
TODO: Move to scripts outside bananalyzer to remove nanoid dependency
"""


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
    url: str, example_dir_path: str, scraper: harambe.AsyncScraperType
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
        sdk = harambe.SDK(
            cast(AbstractPage[PlaywrightElementHandle], page), observer=observer
        )
        sdk._scraper = scraper
        await scraper(sdk, url, {})

        await context.close()

    return observer


def write_examples_to_file(
    examples: list[Example], file_name: str = "./static/examples.json"
) -> None:
    with open(file_name, "r+") as file:
        current_data = json.load(file)
        current_data.extend(
            [
                example.model_dump(exclude_unset=True, exclude_none=True)
                for example in examples
            ]
        )
        file.seek(0)
        file.truncate()
        json.dump(current_data, file, indent=2)


def upload_har_to_s3(har_dir_path: str, s3_bucket_name: str) -> None:
    tar_buffer = BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
        for root, dirs, files in os.walk(har_dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, har_dir_path))
    tar_buffer.seek(0)

    s3 = boto3.client("s3")
    key = f"{os.path.basename(har_dir_path)}.tar.gz"

    s3.upload_fileobj(tar_buffer, s3_bucket_name, key)
    shutil.rmtree(har_dir_path)


async def create_end2end_examples(
    base_url: str,
    metadata: dict[str, str],
    listing_scraper: harambe.AsyncScraperType,
    detail_scraper: Optional[harambe.AsyncScraperType],
    s3_bucket_name: Optional[str] = None,
) -> None:
    domain = urlparse(base_url).netloc.replace("www.", "").replace(".", "_")
    resource_path = (
        f"s3://{s3_bucket_name}/{domain}.tar.gz"
        if s3_bucket_name
        else f"{domain}/index.har"
    )

    observer = await create_har(base_url, f"./static/{domain}", listing_scraper)
    enqueued_urls = [url for url, context, options in observer.urls]

    if not enqueued_urls:
        if not observer.data:
            print("Listing enqueued no URLs and extracted no data. Exiting.")
            return

        data = observer.data
        for row in data:
            row.pop("__url", None)

        print("Listing enqueued no URLs. Creating 1 links_fetch example.")
        examples = [
            Example(
                id=create_nano_id(),
                url=base_url,
                resource_path=resource_path,
                source="har",
                category=metadata["category"],
                subcategory=metadata["subcategory"],
                type="listing_detail",
                goal=metadata["goal"],
                evals=[{"type": "json_match", "expected": data}],
            )
        ]

        write_examples_to_file(examples)

    print(f"Listing enqueued {len(enqueued_urls)} URLs. Creating 1 links example.")
    examples = [
        Example(
            id=create_nano_id(),
            url=base_url,
            resource_path=resource_path,
            source="har",
            category=metadata["category"],
            subcategory=metadata["subcategory"],
            type="listing_detail",
            goal=metadata["goal"],
            evals=[{"type": "json_match", "expected": enqueued_urls}],
        )
    ]

    if not detail_scraper:
        write_examples_to_file(examples)
        return

    enqueued_urls = enqueued_urls[:3]

    print(f"Creating {len(enqueued_urls)} fetch examples from enqueued URLs.")
    for i, url in enumerate(enqueued_urls):
        observer = await create_har(url, f"./static/{domain}_detail{i}", detail_scraper)
        observer_data = observer.data[0]
        observer_data.pop("__url")

        examples.append(
            Example(
                id=create_nano_id(),
                url=url,
                resource_path=resource_path,
                source="har",
                category=metadata["category"],
                subcategory=metadata["subcategory"],
                type="detail",
                fetch_id=metadata["fetch_id"],
                evals=[{"type": "json_match", "expected": observer_data}],
            )
        )

    fuse_hars(
        f"./static/{domain}/index.har",
        [f"./static/{domain}_detail{i}/index.har" for i in range(len(enqueued_urls))],
    )

    write_examples_to_file(examples)

    if s3_bucket_name:
        upload_har_to_s3(f"./static/{domain}", s3_bucket_name)


# if __name__ == "__main__":
#     import asyncio

#     base_url = "https://horizon.adams12.org/our-school/staff-directory"
#     metadata = {
#         "category": "education",
#         "subcategory": "contact",
#         "fetch_id": "job_posting",
#         "type": "listing_detail",
#         "goal": 'Extract the contact information of all members of the school faculty from the given URL. You do not have to navigate to the staff directory page as the URL is the staff directory page. Ensure you paginate. Pagination controls can look like a series of numbers in a row at the bottom of data lists. Do not click random buttons. If the data is not on the page then leave it as null. The information of a single individual should be clustered together. Retrieve information with the following schema {"first_name": {"type": "string"}, "last_name": {"type": "string"} "title": {"type": "string", "description": "The title or role of the individual within the school"}, "phone_number": {"type": "string", "description": "Keep phone number formatting but do not include irrelevant text"}, "email": {"type": "string", "description": "The email address of the individual"}}',
#     }

#     asyncio.run(
#         create_end2end_examples(
#             base_url, metadata, scrape_listing, None, "bananalyzer-examples"
#         )
#     )
