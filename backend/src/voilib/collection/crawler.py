# Copyright (c) 2022-2024 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Main high-level data collection related functions.

It offers functions to retrieve poscast channels and episodes.
"""

from __future__ import annotations

import importlib.resources
import json
import logging
from typing import Optional

from voilib import models, storage
from voilib.collection import feed, local

logger = logging.getLogger(__name__)


def default_channels() -> list[dict]:
    """Return list of default hardcoded podcast feeds"""
    with importlib.resources.open_text("voilib.collection", "urls.json") as f:
        data = json.load(f)
    return data


async def get_or_create_channel(
    feed_url: str, language: str | None = None
) -> tuple[bool, models.Channel | None]:
    """Read a feed url and return its corresponding channel object,
    creating it if needed or retrieving it from the database if it
    already exists.

    """
    logger.info(f"get or create channel from url: {feed_url}, lang {language}")
    created = False
    ch = await models.Channel.objects.get_or_none(feed=feed_url)
    if ch is None:
        created = True
        logger.info(f"creating the channel from url {feed_url}...")
        ch = feed.read_channel(feed_url, language)
        ch = await ch.save() if ch else None
    return created, ch


async def add_default_channels() -> int:
    """Add all the default channels hardcoded in Voilib's code (see
    urls.json)

    Return the number of channels added

    """
    logger.info("adding all the Voilib default channels ")
    total = 0
    for podcast in default_channels():
        url = podcast["url"]
        lang = podcast.get("language", None)
        logger.info(f"get or create channel {url}, lang {lang}")
        created, channel = await get_or_create_channel(podcast["url"], lang)
        total += 1 if created and channel else 0
    logger.info(f"finished adding default channels: {total}")
    return total


async def get_or_create_local_channel(info: dict) -> tuple[bool, models.Channel]:
    created = False
    logger.info(f"get or create local channel from folder {info['folder']}")
    ch = await models.Channel.objects.get_or_none(local_folder=info["folder"])
    if ch is None:
        created, ch = True, await local.read_local_channel(info).save()
    return created, ch


async def add_local_channels() -> int:
    """Add all the channels configured in the local sources file from
    local folder.

    Return the number of channels added.

    """
    logger.info("adding channels from local folder")
    total = 0
    if storage.LOCAL_SOURCES_PATH.exists():
        for channel_info in json.loads(storage.LOCAL_SOURCES_PATH.read_bytes()):
            created, _ = await get_or_create_local_channel(channel_info)
            total += 1 if created else 0
    return total


async def _maybe_add_episode(
    channel: models.Channel, episode: models.Episode
) -> Optional[models.Episode]:
    # add a new episode only if it doesn't exist yet (if exists, return None)
    existing = await models.Episode.objects.get_or_none(url=episode.url)
    if existing is not None:
        logger.debug(f"ignoring episode {episode.id} as it already exists")
        return None
    else:
        logger.info(f"creating episode {episode.title} in channel {channel.id}")
        # this will perform episode's save
        await channel.episodes.add(episode)
        return episode


async def update_channel(
    channel: models.Channel, max_new_episodes: Optional[int] = None
) -> int:
    """Read a channel feed and store all the new added episodes.
    Return the number of episodes added.
    """
    logger.info(f"updating channel {channel.title}")
    if channel.local_folder != "":  # channel from local folder
        episodes = local.read_local_episodes(channel)
    else:  # channel from rss feed
        episodes = feed.read_episodes(channel)
    new_added = 0
    for ep in episodes:
        added = await _maybe_add_episode(channel, ep)
        new_added += 1 if added else 0
        if max_new_episodes and new_added == max_new_episodes:
            break
    return new_added
