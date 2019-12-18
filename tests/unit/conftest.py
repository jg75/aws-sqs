"""Fixtures for testing handlers."""
from botocore.stub import Stubber

import pytest


import consumer.app
import producer.app


@pytest.fixture()
def s3_stub(request):
    stub = Stubber(consumer.app.s3_client)
    request.addfinalizer(stub.assert_no_pending_responses)
    return stub


@pytest.fixture()
def sqs_stub(request):
    stub = Stubber(producer.app.sqs_client)
    request.addfinalizer(stub.assert_no_pending_responses)
    return stub


@pytest.fixture()
def queue_name():
    return "test-queue"


@pytest.fixture()
def message():
    return "Test Request"


@pytest.fixture()
def message_attributes():
    return next(producer.app.generate_message_attributes())


@pytest.fixture(autouse=True)
def mock_s3_bucket(monkeypatch, request):
    original_bucket = consumer.app.bucket
    mock_bucket = "mock-bucket"
    monkeypatch.setattr(consumer.app, "bucket", mock_bucket)

    def _reset_bucket():
        monkeypatch.setattr(consumer.app, "bucket", original_bucket)

    request.addfinalizer(_reset_bucket)

    return mock_bucket


@pytest.fixture()
def s3_key(message_attributes):
    return message_attributes["key"]["StringValue"]


@pytest.fixture()
def single_message_event(s3_key):
    return {
        "Records": [{
            "messageAttributes": {
                "key": {
                    "stringValue": s3_key
                }
            }
        }]
    }


@pytest.fixture()
def context():
    return {}
