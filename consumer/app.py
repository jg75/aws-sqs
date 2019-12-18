"""AWS SQS Queue consumer Lambda."""
from datetime import datetime, timedelta
from json import dumps
import logging
from os import getenv

from boto3 import client


s3_client = client("s3")
bucket = getenv("S3_BUCKET")

logging.basicConfig(level=logging.INFO)


def handler(event, context):
    """Lambda handler for AWS SQS queue consumer."""
    for record in event["Records"]:
        key = record["messageAttributes"]["key"]["stringValue"]
        expires = datetime.now() + timedelta(days=7)
        response = s3_client.put_object(
            Bucket=bucket, Key=key, Expires=expires, ContentType="text/plain"
        )

        logging.info(response)
