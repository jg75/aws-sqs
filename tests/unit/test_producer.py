"""Test producer."""
from botocore.stub import ANY
import pytest

from producer.app import generate_messages


@pytest.mark.unit
def test_producer(sqs_stub, queue_name, message):
    count = 2

    sqs_stub.add_response(
        "get_queue_url",
        {"QueueUrl": queue_name},
        expected_params={"QueueName": queue_name}
    )

    for _ in range(count):
        sqs_stub.add_response(
            "send_message",
            {},
            expected_params={
                "QueueUrl": queue_name,
                "MessageBody": message,
                "MessageAttributes": ANY
            }
        )

    with sqs_stub:
        generate_messages(queue_name, message, count=count)
