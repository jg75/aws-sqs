"""Fixtures for testing handlers."""
from botocore.stub import Stubber
import pytest

import consumer.app
import canary.app


@pytest.fixture()
def s3_stub(request):
    stub = Stubber(consumer.app.s3_client)
    request.addfinalizer(stub.assert_no_pending_responses)
    return stub


@pytest.fixture()
def sqs_stub(request):
    stub = Stubber(canary.app.sqs_client)
    request.addfinalizer(stub.assert_no_pending_responses)
    return stub


@pytest.fixture(autouse=True)
def mock_sqs_queue_url(monkeypatch, request):
    original_queue_url = canary.app.queue_url
    mock_queue_url = "mock-queue-url"
    monkeypatch.setattr(canary.app, "queue_url", mock_queue_url)

    def _reset_queue_url():
        monkeypatch.setattr(canary.app, "queue_url", original_queue_url)

    request.addfinalizer(_reset_queue_url)

    return mock_queue_url


@pytest.fixture(autouse=True)
def mock_message_count(monkeypatch, request):
    original_message_count = canary.app.message_count
    mock_message_count = 100
    monkeypatch.setattr(canary.app, "message_count", mock_message_count)

    def _reset_message_count():
        monkeypatch.setattr(canary.app, "message_count", original_message_count)

    request.addfinalizer(_reset_message_count)

    return mock_message_count


@pytest.fixture(autouse=True)
def mock_message_body(monkeypatch, request):
    original_message_body = canary.app.message_body
    mock_message_body = "Unit Test Message"
    monkeypatch.setattr(canary.app, "message_body", mock_message_body)

    def _reset_message_body():
        monkeypatch.setattr(canary.app, "message_body", original_message_body)

    request.addfinalizer(_reset_message_body)

    return mock_message_body


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
def message_attributes():
    return next(canary.app.generate_message_attributes())


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
def event():
    return {}


@pytest.fixture()
def context():
    return {}
