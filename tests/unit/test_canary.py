"""Test canary."""
from botocore.stub import ANY
import pytest

import canary.app


@pytest.mark.unit
def test_message_attributes_generator():
    """
    Assert that message attributes are well formed.

    {
        "string": {
            "DataType": String|StringList|Number|Binary|BinaryList,
            "StringValue: "string",
            "StringListValue: "string",
            "BinaryValue: "string",
            "BinaryList: "string"
        },
        "key": {
            "DataType": "String",
            "StringValue": "prefix/key"
        }
    }
    """
    attributes = next(canary.app.handler.message_attributes_generator())
    data_types = {
        "String": "StringValue",
        "StringList": "StringListValue",
        "Number": "StringValue",
        "Binary": "BinaryValue",
        "BinaryList": "BinaryListValue",
    }

    for attribute in attributes.values():
        key = data_types[attribute["DataType"]]

        assert attribute[key]


@pytest.mark.unit
def test_canary(sqs_stub, event, context):
    """Assert that the canary is able to send a number of queue messages."""
    queue_url = "test-queue"
    message_count = 100
    message_body = "Test Message"
    handler = canary.app.LambdaHandler(
        sqs_client=canary.app.sqs_client,
        queue_url=queue_url,
        message_count=message_count,
        message_body=message_body,
        message_prefix="prefix",
        message_key="key",
    )

    for _ in range(message_count):
        sqs_stub.add_response(
            "send_message",
            {},
            expected_params={
                "QueueUrl": queue_url,
                "MessageBody": message_body,
                "MessageAttributes": next(handler.message_attributes_generator()),
            },
        )

    with sqs_stub:
        handler(event, context)
