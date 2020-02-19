import boto3
import logging
import sys
from botocore.exceptions import ClientError
from .config import ALERT_SENDER, ALERT_RECIPIENT, ALERT_BODY, ALERT_SUBJECT, SES_CONFIGURATION_SET, AWS_REGION
from string import Template

logger = logging.getLogger('mailer')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

SUBJECT_TMPL = Template(ALERT_SUBJECT)
BODY_TMPL = Template(ALERT_BODY)

CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)


def fake_send(name, mem_usage, mem_util):
    subject = SUBJECT_TMPL.substitute(container=name, mem_util=mem_util, mem_usage=mem_usage)
    body = BODY_TMPL.substitute(container=name, mem_util=mem_util, mem_usage=mem_usage)
    logger.info(subject)
    logger.info(body)


def send_alert(name, mem_usage, mem_util):
    logger.info("Sending alert...")
    subject = SUBJECT_TMPL.substitute(container=name, mem_util=mem_util, mem_usage=mem_usage)
    body = BODY_TMPL.substitute(container=name, mem_util=mem_util, mem_usage=mem_usage)
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
