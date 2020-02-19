from dotenv import load_dotenv
import os
import sys

load_dotenv()

CONTAINER_NAME = os.getenv("CONTAINER_NAME") or sys.exit("Missing CONTAINER_NAME env var")
INTERVAL = int(os.getenv("INTERVAL") or sys.exit("Missing INTERVAL env var"))
MEM_UTIL_THRESHOLD = float(os.getenv("MEM_UTIL_THRESHOLD") or sys.exit("Missing MEM_UTIL_THRESHOLD env var"))
print(MEM_UTIL_THRESHOLD)
ALERT_SENDER = os.getenv("ALERT_SENDER") or sys.exit("Missing ALERT_SENDER env var")
ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT") or sys.exit("Missing ALERT_RECIPIENT env var")
ALERT_SUBJECT = os.getenv("ALERT_SUBJECT") or sys.exit("Missing ALERT_SUBJECT env var")
ALERT_BODY = os.getenv("ALERT_BODY") or sys.exit("Missing ALERT_BODY env var")

SES_CONFIGURATION_SET = os.getenv("SES_CONFIGURATION_SET") or sys.exit("Missing SES_CONFIGURATION_SET env var")
AWS_REGION = os.getenv("AWS_REGION") or sys.exit("Missing AWS_REGION env var")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") or sys.exit("Missing AWS_ACCESS_KEY_ID env var")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") or sys.exit("Missing AWS_SECRET_ACCESS_KEY env var")
