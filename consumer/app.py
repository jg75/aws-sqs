"""AWS SQS Queue consumer Lambda."""
from datetime import datetime, timedelta
from json import dumps
from logging import getLogger, INFO, StreamHandler
from os import getenv
from boto3 import client


class LambdaHandler:
    """
    The Lambda handler.

    Handle incoming events. Events can be multiple record batches.
    Each record should contain a prefix/key to identify the output.
    """

    @staticmethod
    def get_key(record):
        """Get the key from the message attributes."""
        return record["messageAttributes"]["key"]["stringValue"]

    def __init__(self, s3_client, s3_bucket, s3_object_ttl=None):
        """Override."""
        self.s3_client = s3_client
        self.s3_bucket = s3_bucket
        self.s3_object_ttl = s3_object_ttl if s3_object_ttl else timedelta(days=7)
        self.logger = getLogger("__name__")
        stream_handler = StreamHandler()

        stream_handler.setLevel(INFO)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(INFO)

    def __call__(self, event, context):
        """Override."""
        for record in event["Records"]:
            response = self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=self.get_key(record),
                Expires=datetime.now() + self.s3_object_ttl,
                ContentType="text/plain",
            )

            self.logger.info(response)


s3_client = client("s3")
handler = LambdaHandler(s3_client=s3_client, s3_bucket=getenv("S3_BUCKET"))
