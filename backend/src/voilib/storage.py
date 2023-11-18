# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

""" File storage related functions

"""
import functools
import logging
import pathlib
import shutil

import requests  # type: ignore

from voilib import settings, storage
from voilib.models import media
from voilib.utils import slugify

DEFAULT_EPISODES_SUFFIX: str = "mp3"

LOCAL_CHANNELS_PATH = settings.settings.data_dir / "local"
LOCAL_SOURCES_PATH = LOCAL_CHANNELS_PATH / "sources.json"

logger = logging.getLogger(__name__)


@functools.cache
def vectordb_path() -> pathlib.Path:
    """Return the path of the vector database, for cases when we use a
    file to store it (usually, in tests).

    """
    path = settings.settings.data_dir / "vector"
    path.mkdir(exist_ok=True)
    return path


def channel_path(channel: media.Channel) -> pathlib.Path:
    """Return the path where channel media files should be stored."""
    fname = f"{slugify(channel.title[:30])}-{slugify(channel.feed[-10:])}"
    return settings.settings.media_folder / fname


async def episode_file(
    episode: media.Episode, create_channel_folder: bool = False
) -> pathlib.Path:
    """Return path where episode should be stored."""
    path = channel_path(await episode.channel.load())  # type: ignore
    if create_channel_folder and not path.exists():
        path.mkdir(parents=True)
    fname = f"{slugify(episode.title[:30])}-{slugify(episode.url[-10:])}"
    return (path / fname).with_suffix(f".{DEFAULT_EPISODES_SUFFIX}")


async def fetch_file(url: str, output_file: pathlib.Path) -> pathlib.Path:
    """Fetch file from a given url and store it in output_file"""
    logger.info(f"downloading file from url {url}")
    data = requests.get(url, allow_redirects=True).content
    with output_file.open("wb") as f:
        f.write(data)
    return output_file


async def transcription_file(
    episode: media.Episode,
) -> pathlib.Path:
    """Return file where episode transcription should be stored"""
    efile = await episode_file(episode)
    return efile.with_suffix(".csv")


async def download_episode(episode: media.Episode) -> pathlib.Path:
    """Download the audio file associated to a given episode.

    If it is an episode from a local folder, it will move its
    corresponding file to the media folder.

    If it already exists, just return it.

    """
    logger.info(f"checking if we need to download episode {episode.id}")
    channel = await episode.channel.load()  # type: ignore
    audio = await episode_file(episode, create_channel_folder=True)
    if audio.exists():
        return audio
    if not audio.exists():
        if channel.local_folder != "":  # channel from local folder:
            local_file = storage.LOCAL_CHANNELS_PATH / episode.url
            shutil.copy(local_file, audio)
        else:  # channel from rss feed
            await fetch_file(episode.url, audio)
    return audio
