# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Mixed utilities

Everything can be considered an utility, so let's try to keep this as
small as possible.

"""
import re
import unicodedata


def slugify(value: str) -> str:
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub("[^\w\s-]", "", value).strip().lower()  # noqa
    return re.sub("[-\s]+", "-", value)  # noqa
