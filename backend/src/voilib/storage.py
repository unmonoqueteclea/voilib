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

LOCAL_CHANNELS_PATH = settings.settings.data_dir / "local"
MEDIA_PATH = settings.settings.data_dir / "media"
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
    efile = storage.MEDIA_PATH / episode.filename
    return efile.with_suffix(".csv")


async def download_episode(episode: media.Episode) -> pathlib.Path:
    """Download the audio file associated to a given episode.

    If it is an episode from a local folder, it will move its
    corresponding file to the media folder.

    If it already exists, just return it.

    """
    logger.info(f"checking if we need to download episode {episode.id}")
    channel = await episode.channel.load()  # type: ignore

    channel_path: pathlib.Path = storage.MEDIA_PATH / channel.title
    if not channel_path.exists():
        channel_path.mkdir(parents=True)

    episode_audio_file: pathlib.Path = channel_path / episode.filename
    if episode_audio_file.exists():
        return episode_audio_file
    else:
        if channel.local_folder != "":  # channel from local folder:
            local_file: pathlib.Path = storage.LOCAL_CHANNELS_PATH / channel.title / episode.filename
            if local_file.exists():
                logger.info(f"Copying local file: {str(local_file)}")
                shutil.copy(local_file, episode_audio_file)
            else:
                logger.warning(f"Missing local file: {str(local_file)}")
        else:  # channel from rss feed
            await fetch_file(episode.url, episode_audio_file)

    return episode_audio_file
