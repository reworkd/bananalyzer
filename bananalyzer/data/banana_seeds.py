import json
from typing import Any, Dict, List

import boto3

s3 = boto3.client("s3", region_name="us-east-1")


def download_examples_from_s3(examples_bucket: str) -> List[Dict[str, Any]]:
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


def download_mhtml(url: str) -> str:
    if url.startswith("s3://"):
        s3 = boto3.resource("s3")

        bucket_name = url.split("/")[2]
        key = "/".join(url.split("/")[3:])

        obj = s3.Object(bucket_name, key)
        mhtml = obj.get()["Body"].read().decode("utf-8")

        return mhtml
    else:
        raise NotImplementedError("Only s3:// URIs are currently supported")
