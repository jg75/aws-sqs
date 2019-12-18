"""AWS SQS message producer."""
from datetime import datetime
from logging import getLogger, INFO, StreamHandler
from sys import argv
from uuid import uuid4

from boto3 import client


sqs_client = client("sqs")
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


def generate_messages(queue_name, message_body, count=100):
    """Send messages with message attributes to a queue."""
    response = sqs_client.get_queue_url(QueueName=queue_name)
    queue_url = response["QueueUrl"]

    for _ in range(count):
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=next(generate_message_attributes()),
        )

        logger.info(response)


if __name__ == "__main__":
    for queue_name in argv[1:]:
        generate_messages(queue_name, "Message Body")
