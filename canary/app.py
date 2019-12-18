"""AWS SQS message canary."""
from datetime import datetime
from logging import getLogger, INFO, StreamHandler
from os import getenv
from uuid import uuid4

from boto3 import client


sqs_client = client("sqs")
queue_url = getenv("QUEUE_URL")
message_count = int(getenv("MESSAGE_COUNT", 100))
message_body = getenv("MESSAGE_BODY")
logger = getLogger("__name__")
stream_handler = StreamHandler()

stream_handler.setLevel(INFO)
logger.addHandler(stream_handler)
logger.setLevel(INFO)


def generate_message_attributes():
    """Generate message attributes for messages."""
    prefix = datetime.now().strftime("%Y%m%d%H%M")
    key = str(uuid4())

    yield {"key": {"DataType": "String", "StringValue": f"{prefix}/{key}"}}


def handler(event, context):
    """Lambda handler for AWS SQS queue canary."""
    for _ in range(message_count):
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=next(generate_message_attributes()),
        )

        logger.info(response)
