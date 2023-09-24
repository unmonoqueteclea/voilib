# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Mixed utilities

Everything can be considered an utility, so let's try to keep this as
small as possible.

"""
import typing
import re
import time
import unicodedata

from voilib import settings


def slugify(value: str) -> str:
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub("[^\w\s-]", "", value).strip().lower()  # noqa
    return re.sub("[-\s]+", "-", value)  # noqa


def log_event(key: str, info: str) -> None:
    redis = settings.settings.redis_cache
    redis.set(key, f"{time.time()}|{info}")


def get_event(key: str) -> typing.Optional[dict]:
    redis = settings.settings.redis_cache
    event = redis.get(key)
    if event:
        return {"time": event.split("|")[0], "info": event.split("|")[1]}
    return
