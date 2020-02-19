import boto3
import logging
import sys
from botocore.exceptions import ClientError
from .config import ALERT_SENDER, ALERT_RECIPIENT, SES_CONFIGURATION_SET, AWS_REGION

logger = logging.getLogger('mailer')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

SUBJECT = "Docker container %s memory utilization has reached %d%%"
BODY_TEXT = "Container %s is currently using %d%% of the available memory. Restart ASAP."

CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)


def fake_send(name, mem_usage, mem_util):
    subject = SUBJECT % (name, mem_util)
    body = BODY_TEXT % (mem_util, name)
    logger.info(subject)
    logger.info(body)


def send_alert(name, mem_usage, mem_util):
    logger.info("Sending alert...")
    subject = SUBJECT % (name, mem_util)
    body = BODY_TEXT % (name, mem_util)
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    ALERT_RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=ALERT_SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=SES_CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
    else:
        logger.info("Message ID: " + response['MessageId'])
