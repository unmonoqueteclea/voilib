# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Functions to deal with channels imported from local files in
filesystem.

"""
import logging
from datetime import datetime

from voilib import models, storage

logger = logging.getLogger(__name__)


def read_local_channel(info: dict) -> models.Channel:
    """Read a local channel from its config dictionary and return a
    channel object (not stored yet in db). This function won't read
    channel episodes, just some basic metadata about channels.

    """
    logger.info(f"reading local channel from folder: {info['folder']}")
    return models.Channel(
        title=info["name"],
        kind=models.ChannelKind.local.value,
        description=info.get("description", ""),
        language=info["language"],
        url="",
        feed="",
        local_folder=info["folder"],
        image=info.get("image", ""),
    )


def read_local_episodes(channel: models.Channel) -> list[models.Episode]:
    """Return a list with all the episodes (not stored yet in db) from
    a given channel. Currently, only files with extension wav or mp3
    within the channel folder will be considered as episodes.

    """
    logger.info(f"reading local episodes from channel: {channel.id}: {channel.title}")
    channel_folder = storage.LOCAL_CHANNELS_PATH / channel.local_folder
    mp3_files = list(channel_folder.glob("*.mp3"))
    wav_files = list(channel_folder.glob("*.wav"))
    episodes: list[models.Episode] = []
    for ep in mp3_files + wav_files:
        uri = f"{channel.local_folder}/{ep.name}"
        episode = models.Episode(
            title=ep.name,
            guid=uri,
            description="",
            # take date from audio file metadata
            date=datetime.fromtimestamp(ep.stat().st_ctime),
            url=uri,
            episode=-1,
            season=-1,
            duration=None,
            transcribed=False,
            embeddings=False,
        )
        episodes.append(episode)
    logger.info(f"{len(episodes)} episodes parsed from channel {channel.title}")
    return episodes
