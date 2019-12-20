"""AWS SQS message canary."""
from datetime import datetime
from logging import getLogger, INFO, StreamHandler
from os import getenv
from uuid import uuid4
from boto3 import client


class LambdaHandler:
    """
    The Lambda handler.

    Produce dummy messages on a queue to canary test a lambda consumer.
    """

    def message_attributes_generator(self):
        """Generate message attributes for messages."""
        prefix = self.message_arguments.get(
            "message_prefix", datetime.now().strftime("%Y%m%d%H%M")
        )
        key = self.message_arguments.get("message_key", str(uuid4()))

        yield {"key": {"DataType": "String", "StringValue": f"{prefix}/{key}"}}

    def __init__(self, sqs_client, queue_url, generator=None, **message_arguments):
        """Override."""
        self.sqs_client = sqs_client
        self.queue_url = queue_url
        self.generator = generator if generator else self.message_attributes_generator
        self.message_arguments = message_arguments
        self.logger = getLogger("__name__")
        stream_handler = StreamHandler()

        stream_handler.setLevel(INFO)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(INFO)

    def __call__(self, event, context):
        """Override."""
        for _ in range(self.message_arguments["message_count"]):
            response = sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=self.message_arguments["message_body"],
                MessageAttributes=next(self.message_attributes_generator()),
            )

            self.logger.info(response)


sqs_client = client("sqs")
handler = LambdaHandler(
    sqs_client=sqs_client,
    queue_url=getenv("QUEUE_URL"),
    message_count=int(getenv("MESSAGE_COUNT", "100")),
    message_body=getenv("MESSAGE_BODY", "Canary Test"),
)
