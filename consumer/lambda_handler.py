"""AWS SQS Queue consumer Lambda."""
from json import dumps
from os import getenv


BUCKET = os.getenv("S3_BUCKET")


def handler(event, context):
    for record in event["Records"]:
        print(dumps(record['dynamodb'], indent=2))
