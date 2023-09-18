# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Generate episode transcriptions

"""
import csv
import functools
import logging
import pathlib
import time

from faster_whisper import WhisperModel

from voilib import storage, utils
from voilib.models import media

logger = logging.getLogger(__name__)
TRANSCRIBER_MODEL: str = "small"
Transcription = list[tuple[float, float, str]]


@functools.cache
def _get_model() -> WhisperModel:
    logger.info("loading transcription model object")
    return WhisperModel(TRANSCRIBER_MODEL, device="cpu", compute_type="int8")


def transcribe(audio: pathlib.Path) -> Transcription:
    """Given an audio path, transcribe it and return a list where each
    element has the following format:

    (start_time [float], end_time [float], transcription [str])
    """
    logger.info(f"start transcription of file {audio}")
    start_time = time.time()
    model = _get_model()
    segments, info = model.transcribe(str(audio))
    end_time = time.time()
    transcription = [(s.start, s.end, s.text) for s in segments]
    logger.info(f"end transcription of file {audio} in {end_time-start_time} seconds")
    return transcription


def store_transcription(transcription: Transcription, path: pathlib.Path) -> None:
    """Store a transcription as a simple CSV file."""
    with path.open(mode="w") as csvfile:
        writer = csv.writer(csvfile, delimiter="|", quotechar='"')
        writer.writerows(transcription)
    return


def read_transcription(path: pathlib.Path) -> Transcription:
    """Read a transcription from a given path"""
    rows = []
    with path.open() as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        for row in reader:
            start = float(row[0])
            # sometimes the end is not defined
            end = float(row[1]) if len(row[1]) > 0 else start
            rows.append((start, end, row[2]))
    return rows


async def transcribe_episode(episode: media.Episode) -> pathlib.Path:
    """Download and transcribe (if needed) a given episode, returning
    the path of the generated transcription file.

    """
    title = episode.title
    logger.info(f"transcription of episode {title}: {episode.pk}")
    utils.log_event("event_transcription_start", title)
    trfile = await storage.transcription_file(episode)
    if not trfile.exists():
        audio = await storage.download_episode(episode)
        store_transcription(transcribe(audio), trfile)
        audio.unlink(missing_ok=True)
    if not episode.transcribed:
        episode.transcribed = True
        await episode.update()
    utils.log_event("event_transcription_end", title)
    logger.info(f"transcription of episode {title} finished")
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
