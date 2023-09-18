# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Functions to collect channels and episodes.

- Module crawler is the module that will retrieve podcast channels and
  episodes and create the corresponding app models.

- Module feed contains some functions to deal with RSS podcasts feeds
  and return channel or episode objects (not stored yet in db)
"""

from .crawler import add_default_channels  # noqa
from .crawler import default_channels  # noqa
from .crawler import get_or_create_channel  # noqa
from .crawler import update_channel  # noqa
from .feed import read_channel, read_episodes  # noqa
