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


async def create_end2end_examples(
    base_url: str,
    metadata: dict[str, str],
    listing_scraper: harambe.AsyncScraperType,
    detail_scraper: harambe.AsyncScraperType,
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

    examples = [
        Example(
            id=create_nano_id(),
            url=base_url,
            resource_path=resource_path,
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
                resource_path=resource_path,
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

    with open("./static/examples.json", "r+") as file:
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

    if s3_bucket_name:
        upload_har_to_s3(f"./static/{domain}", s3_bucket_name)


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


async def scrape_listing(
    sdk: harambe.SDK, current_url: str, *args: Any, **kwargs: Any
) -> None:
    page: Page = sdk.page
    await page.wait_for_timeout(2000)
    await page.wait_for_selector(".information")
    faculty_rows = await page.query_selector_all(".information a.au-target")
    for row in faculty_rows:
        next_url = await row.get_attribute("href")
        if next_url:
            await sdk.enqueue(next_url)

    async def pager() -> Optional[str | ElementHandle]:
        next_page_link = await page.query_selector(
            '.pagination > li > a[data-ph-tevent-attr-trait214="Next"]'
        )
        return next_page_link

    await sdk.paginate(pager)


async def scrape_detail(
    sdk: harambe.SDK, current_url: str, *args: Any, **kwargs: Any
) -> None:
    page: Page = sdk.page
    await page.wait_for_load_state("networkidle")
    await page.wait_for_selector("h1.job-title")
    title_element = await page.query_selector("h1.job-title")
    department_element = await page.query_selector(".job-category")
    job_id_element = await page.query_selector(".jobId")
    job_description_element = await page.query_selector(".job-description")
    locations_elements = await page.query_selector_all(".au-target.cityState")
    employment_type_element = await page.query_selector(".au-target.type")
    apply_url_element = await page.query_selector('a[title="Apply Now"]')
    language_element = await page.query_selector("html")
    skills_element = await page.query_selector(
        '.job-description p:has-text("Responsibilities")'
    )
    qualifications_element = await page.query_selector(
        '.job-description p:has-text("Required"), .job-description p:has-text("Requirements"), .job-description p:has-text("Qualifications")'
    )
    preferred_skills_element = await page.query_selector(
        '.job-description p:has-text("Preferred")'
    )
    ul_elements = await page.query_selector_all(".job-description ul")
    qualifications = (
        await qualifications_element.evaluate(
            """(element) => {
        let nextSibling = element.nextElementSibling;
            while (nextSibling) {
                if (nextSibling.tagName === "UL") {
                    return nextSibling.textContent;
                }
                nextSibling = nextSibling.nextElementSibling;
            }
            return null; // If no next <ul> tag is found
        }"""
        )
        if qualifications_element
        else None
    )

    preferred_skills = (
        await preferred_skills_element.evaluate(
            """(element) => {
        let nextSibling = element.nextElementSibling;
            while (nextSibling) {
                if (nextSibling.tagName === "UL") {
                    return nextSibling.textContent;
                }
                nextSibling = nextSibling.nextElementSibling;
            }
            return null; // If no next <ul> tag is found
        }"""
        )
        if preferred_skills_element
        else None
    )

    skills = (
        await skills_element.evaluate(
            """(element) => {
        let nextSibling = element.nextElementSibling;
            while (nextSibling) {
                if (nextSibling.tagName === "UL") {
                    return nextSibling.textContent;
                }
                nextSibling = nextSibling.nextElementSibling;
            }
            return null; // If no next <ul> tag is found
        }"""
        )
        if skills_element
        else None
    )

    if not qualifications:
        qualifications = (
            await ul_elements[1].text_content()
            if ul_elements and len(ul_elements) > 1
            else None
        )
    if not skills:
        skills = await ul_elements[0].text_content() if ul_elements else None
    if not preferred_skills:
        preferred_skills = (
            await ul_elements[2].text_content()
            if ul_elements and len(ul_elements) > 2
            else None
        )

    job_id = await job_id_element.inner_text() if job_id_element else None
    job_id = job_id.split("\n")[-1].strip() if job_id else job_id
    title = await title_element.inner_text() if title_element else None
    department = await department_element.inner_text() if department_element else None
    department = department.split("\n")[-1].strip() if department else department
    job_description = (
        await job_description_element.inner_text() if job_description_element else None
    )
    locations = [await x.inner_text() for x in locations_elements if x]
    sub_points = job_description.split("\n\n") if job_description else []
    sub_points = [x for x in sub_points if x.strip()]
    job_benefits = (
        " ".join(
            [
                x
                for x in sub_points
                if "benefits" in x.lower() or "compensation" in x.lower()
            ]
        )
        if [
            x
            for x in sub_points
            if "benefits" in x.lower() or "compensation" in x.lower()
        ]
        else None
    )
    apply_url = (
        await apply_url_element.get_attribute("href") if apply_url_element else None
    )
    employment_type = (
        await employment_type_element.inner_text() if employment_type_element else None
    )
    employment_type = (
        employment_type.split("\n")[-1].strip() if employment_type else employment_type
    )
    language = (
        await language_element.get_attribute("lang") if language_element else None
    )
    await sdk.save_data(
        {
            "job_id": job_id,
            "department": department,
            "title": title,
            "job_description": job_description,
            "locations": locations,
            "job_type": None,
            "date_posted": None,
            "apply_url": apply_url,
            "job_benefits": job_benefits,
            "qualifications": qualifications,
            "preferred_skills": preferred_skills,
            "skills": skills,
            "recruiter_email": None,
            "application_deadline": None,
            "language": language,
            "employment_type": employment_type,
            "tags": [],
        }
    )
