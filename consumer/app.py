"""AWS SQS Queue consumer Lambda."""
from datetime import datetime, timedelta
from json import dumps
from logging import getLogger, INFO, StreamHandler
from os import getenv

from boto3 import client


s3_client = client("s3")
bucket = getenv("S3_BUCKET")
logger = getLogger("__name__")
stream_handler = StreamHandler()

stream_handler.setLevel(INFO)
logger.addHandler(stream_handler)
logger.setLevel(INFO)


def handler(event, context):
    """Lambda handler for AWS SQS queue consumer."""
    for record in event["Records"]:
        key = record["messageAttributes"]["key"]["stringValue"]
        expires = datetime.now() + timedelta(days=7)
        response = s3_client.put_object(
            Bucket=bucket, Key=key, Expires=expires, ContentType="text/plain"
        )

        logger.info(response)
