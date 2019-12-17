"""AWS SQS Producer."""
from boto3 import resource

sqs = resource("sqs")
sqs_client = sqs.meta.client
