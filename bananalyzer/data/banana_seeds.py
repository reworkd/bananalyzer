import json
import os
from typing import Any, Dict, List
import boto3


def download_examples_from_s3(examples_bucket: str) -> List[Dict[str, Any]]:
    s3 = boto3.client("s3", region_name="us-east-1")

    examples = []
    response = s3.list_objects(Bucket=examples_bucket)
    for file in response["Contents"]:
        key = file["Key"]

        if key.startswith("example-") and key.endswith(".json"):
            response = s3.get_object(Bucket=examples_bucket, Key=key)
            file_content = response["Body"].read().decode("utf-8")
            example = json.loads(file_content)

            if example["fetch_id"] == "":
                del example["fetch_id"]

            for row in example["evals"][0]["expected"]:
                row = {k: v for k, v in row.items() if not k.startswith("__")}
                if "context" in row:
                    for key, value in row["context"].items():
                        row[key] = value
                    del row["context"]

            examples.append(example)

    return examples


def download_mhtml(url: str) -> str:
    s3 = boto3.client("s3", region_name="us-east-1")

    if url.startswith("s3://"):
        bucket_name = url.split("/")[2]
        key = "/".join(url.split("/")[3:])

        response = s3.get_object(Bucket=bucket_name, Key=key)
        mhtml = response["Body"].read().decode("utf-8")

        return mhtml
    else:
        raise NotImplementedError("Only s3:// URIs are currently supported")

def download_har(har_dir_path: str, s3_url: str) -> None:
    s3 = boto3.client("s3", region_name="us-east-1")

    parts = s3_url.split('/')
    bucket_name = parts[2]
    bucket = s3.Bucket(bucket_name) # TODO: make sure this S3 stuff works
    s3_directory_prefix = '/'.join(parts[3:-1]) + '/'

    if not os.path.exists(har_dir_path):
        os.makedirs(har_dir_path)

    for obj in bucket.objects.filter(Prefix=s3_directory_prefix):
        bucket.download_file(obj.key, har_dir_path)
