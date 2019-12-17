"""AWS SQS Queue consumer Lambda."""
from json import dumps
import logging
from os import getenv


BUCKET = getenv("S3_BUCKET")

logging.basicConfig(level=logging.INFO)


def handler(event, context):
    """Lambda handler for AWS SQS queue consumer."""
    for record in event["Records"]:
        print(dumps(record, indent=2))
