from .config import MEM_UTIL_THRESHOLD, CONTAINER_NAME, INTERVAL
from timeloop import Timeloop
from datetime import timedelta
from .stats import process_stats

tl = Timeloop()


@tl.job(interval=timedelta(seconds=INTERVAL))
def run_monitor():
    process_stats(name=CONTAINER_NAME, mem_util_threshold=MEM_UTIL_THRESHOLD)


if __name__ == "__main__":
    tl.start(block=True)
