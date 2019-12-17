"""AWS SQS message producer."""
from datetime import datetime
import logging
from sys import argv
from uuid import uuid4

from producer import sqs_client


logging.basicConfig(level=logging.INFO)


def generate_message_attributes():
    """Generate message attributes for messages."""
    timestamp = datetime.now().strftime("%Y/%m/%d/%H/%M/%S")
    key_prefix = {"DataType": "String", "StringValue": timestamp}
    key = {"DataType": "String", "StringValue": str(uuid4())}

    yield {"key_prefix": key_prefix, "key": key}


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

        logging.info(response)


if __name__ == "__main__":
    for queue_name in argv[1:]:
        generate_messages(queue_name, "Stuff", count=1)
