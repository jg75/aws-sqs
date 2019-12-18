"""Test canary."""
from botocore.stub import ANY
import pytest

import canary.app


@pytest.mark.unit
def test_canary(sqs_stub, event, context):
    for _ in range(canary.app.message_count):
        sqs_stub.add_response(
            "send_message",
            {},
            expected_params={
                "QueueUrl": canary.app.queue_url,
                "MessageBody": canary.app.message_body,
                "MessageAttributes": ANY
            }
        )

    with sqs_stub:
        canary.app.handler(event, context)
