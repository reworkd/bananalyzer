import json
from typing import Any, Dict, List

import boto3
import requests

s3 = boto3.client("s3", region_name="us-east-1")
# TODO: how to handle s3 credentials?


async def download_examples_from_s3(examples_bucket: str) -> List[Dict[str, Any]]:
    examples = []
    response = s3.list_objects(Bucket=examples_bucket)
    for file in response["Contents"]:
        key = file["Key"]

        if key.startswith("example-") and key.endswith(".json"):
            response = s3.get_object(Bucket=examples_bucket, Key=key)
            file_content = response["Body"].read().decode("utf-8")
            example = json.loads(file_content)

            examples.append(example)

    return examples


async def download_mhtml_from_s3(s3_uri: str) -> str:
    mhtml_bucket = "deworkd-prod-traces"
    key = s3_uri.replace("s3://deworkd-prod-traces/", "")
    response = s3.get_object(Bucket=mhtml_bucket, Key=key)
    mhtml = response["Body"].read().decode("utf-8")

    return mhtml


async def download_mhtml(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the GET request was unsuccessful
    mhtml = response.text
    return mhtml
