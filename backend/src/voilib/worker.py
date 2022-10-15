# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

"""RQ worker configuration

"""
import logging

import redis  # type: ignore
from rq import Worker  # type: ignore

from voilib import settings

# without this, we wouldn't be able to see logs in the workers
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # provide the worker with the list of queues (str) to listen to.
    redis_conn = redis.Redis(settings.settings.redis_host)
    w = Worker([settings.queue], connection=redis_conn)
    w.work(with_scheduler=True)
