"""Test consumer."""
from botocore.stub import ANY
import pytest

from consumer.app import handler


@pytest.mark.unit
def test_consumer(s3_stub):
    with s3_stub:
        assert True
