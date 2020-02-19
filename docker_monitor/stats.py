import logging
import os
import sys
from .mail import send_alert
import docker

logger = logging.getLogger('docker_monitor')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

client = docker.from_env()


# https://stackoverflow.com/questions/53764761/inconsistency-between-docker-stats-command-and-docker-rest-api-memory-stats
def real_mem_stats(stats):
    limit = stats["memory_stats"]["limit"]
    mem_usage = stats["memory_stats"]["usage"] - stats["memory_stats"]["stats"]["cache"]
    mem_utilization = round(mem_usage / limit * 100, 2)
    return mem_usage, mem_utilization


def memory_alert(name, usage, util, threshold):
    logger.warning(f'{name} memory utilization is {util}%')
    send_alert(name, usage, util)


def memory_check(stats, threshold):
    name = stats['name']
    usage, util = real_mem_stats(stats)
    logger.info(dict(name=name, mem_usage=usage, mem_util=util, mem_util_threshold=threshold))
    if util > threshold:
        memory_alert(name, usage, util, threshold)


def process_stats(name, mem_util_threshold):
    logger.info(f'Fetching container stats: {name}')
    c = client.containers.get(name)
    stats = c.stats(stream=False)
    memory_check(stats, threshold=mem_util_threshold)
