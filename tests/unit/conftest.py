"""Fixtures for testing handlers."""
from botocore.stub import Stubber

import pytest

import producer
import consumer


@pytest.fixture()
def s3_stub(request):
    stub = Stubber(consumer.s3_client)
    request.addfinalizer(stub.assert_no_pending_responses)
    return stub


@pytest.fixture()
def sqs_stub(request):
    stub = Stubber(producer.sqs_client)
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
