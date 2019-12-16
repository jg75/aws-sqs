"""AWS SQS message producer."""
from datetime import datetime
from uuid import uuid4
from sys import argv

from producer import sqs


def generate_message_attributes():
    yield {
        "message_id": str(uuid4()),
        "message_timestamp": str(datetime.now())
    }


def generate_messages(sqs, queue_name):
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    for message_attributes in generate_message_attributes():
        response = queue.send_message(MessageAttributes=message_attributes)

        print(response)


if __name__ == "__main__":
    for queue_name in argv[1:]:
        generate_messages(sqs, queue_name)
