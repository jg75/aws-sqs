"""AWS SQS Queue Consumer."""
from boto3 import resource


s3 = resource("s3")
s3_client = s3.meta.client
