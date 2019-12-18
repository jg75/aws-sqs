"""Test consumer."""
from botocore.stub import ANY
import pytest

import consumer.app


@pytest.mark.unit
def test_consumer(s3_stub, s3_key, single_message_event, context):
    s3_stub.add_response(
        "put_object",
        {},
        expected_params={
            "Bucket": consumer.app.bucket,
            "Key": s3_key,
            "Expires": ANY,
            "ContentType": "text/plain"
        }
    )

    with s3_stub:
        consumer.app.handler(single_message_event, context)
