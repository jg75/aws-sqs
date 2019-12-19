"""Fixtures for testing handlers."""
from botocore.stub import Stubber
import pytest

import consumer.app
import canary.app


@pytest.fixture()
def sqs_stub(request):
    stub = Stubber(canary.app.sqs_client)
    request.addfinalizer(stub.assert_no_pending_responses)
    return stub


@pytest.fixture()
def s3_stub(request):
    stub = Stubber(consumer.app.s3_client)
    request.addfinalizer(stub.assert_no_pending_responses)
    return stub


@pytest.fixture()
def event():
    return {}


@pytest.fixture()
def context():
    return {}
