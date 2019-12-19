"""Lambda SQS Consumer tests."""
from botocore.stub import ANY
import pytest

import consumer.app


@pytest.mark.unit
def test_consumer(s3_stub, event, context):
    """Assert that the consumer is able to process a batch of messages."""
    s3_bucket = "bucket"
    event = {"Records": []}

    for i in range(10):
        event["Records"].append({
            "messageAttributes": {
                "key": {"stringValue": f"prefix/key{i}"}
            }
        })

        s3_stub.add_response(
            "put_object",
            {},
            expected_params={
                "Bucket": s3_bucket,
                "Key": ANY,
                "Expires": ANY,
                "ContentType": "text/plain"
            }
        )

    with s3_stub:
        handler = consumer.app.LambdaHandler(
            s3_client=consumer.app.s3_client,
            s3_bucket=s3_bucket
        )

        handler(event, context)
