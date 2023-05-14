# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

"""Generate episode transcriptions

"""
import csv
import functools
import logging
import pathlib
import time
import jax.numpy as jnp
from whisper_jax import FlaxWhisperPipline

from voilib import storage
from voilib.models import media

logger = logging.getLogger(__name__)

# https://github.com/sanchit-gandhi/whisper-jax#available-models-and-languages
TRANSCRIBER_MODEL: str = "small"
Transcription = list[tuple[float, float, str]]


@functools.cache
def _get_pipeline() -> FlaxWhisperPipline:
    logger.info("loading transcription pipeline object")
    return FlaxWhisperPipline(
        f"openai/whisper-{TRANSCRIBER_MODEL}",
        # running model computation in half-precision to make it faster
        dtype=jnp.float16,
        batch_size=4,
    )


def transcribe(audio: pathlib.Path) -> Transcription:
    """Given an audio path, transcribe it and return a list where each
    element has the following format:

    (start_time [float], end_time [float], transcription [str])
    """
    logger.info(f"start transcription of file {audio}")
    start_time = time.time()
    pipeline = _get_pipeline()
    output = pipeline(str(audio), task="transcribe", return_timestamps=True)
    end_time = time.time()
    logger.info(f"end transcription of file {audio} in {end_time-start_time}")
    return [(*c["timestamp"], c["text"]) for c in output["chunks"]]  # type: ignore


def store_transcription(transcription: Transcription, path: pathlib.Path) -> None:
    """Store a transcription as a simple CSV file."""
    with path.open(mode="w") as csvfile:
        writer = csv.writer(csvfile, delimiter="|", quotechar='"')
        writer.writerows(transcription)
    return


def read_transcription(path: pathlib.Path) -> Transcription:
    """Read a transcription from a given path"""
    rows = None
    with path.open() as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        rows = [(float(row[0]), float(row[1]), row[2]) for row in reader]
    return rows  # type: ignore


async def transcribe_episode(episode: media.Episode) -> pathlib.Path:
    """Download and transcribe (if needed) a given episode, returning
    the path of the generated transcription file.

    """
    logger.info(f"transcription of episode {episode.title}")
    trfile = await storage.transcription_file(episode)
    if not trfile.exists():
        audio = await storage.download_episode(episode)
        store_transcription(transcribe(audio), trfile)
        audio.unlink(missing_ok=True)
    if not episode.transcribed:
        episode.transcribed = True
        await episode.update()
    logger.info(f"transcription of episode {episode.title} finished")
    return trfile


async def check_all_pending_episodes() -> None:
    """Correct all episodes that are marked as not transcribed but
    have a valid, existing, transcription file.

    """
    logger.info("checking all episodes incorrectly marked as not transcribed")
    updated_num = 0
    for episode in await media.Episode.objects.filter(transcribed=False).all():
        if (await storage.transcription_file(episode)).exists():
            episode.transcribed = True
            await episode.update()
            updated_num += 1
    logger.info(f"finish fixing transcribed field in {updated_num} episodes")
    return
