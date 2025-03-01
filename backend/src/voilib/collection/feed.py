# Copyright (c) 2022-2024 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Utilities to parse podcasts RSS feeds

Functions from this module return Channel or Episode objects, but they
don't interact with the database.
"""

from __future__ import annotations

import logging
import typing
import xml
from datetime import datetime
import re

import dateutil.parser
import requests  # type: ignore
import xmltodict

from voilib import models

IGNORE_EPISODES_TYPES: list[str] = ["bonus", "trailer"]

LANGUAGES_MAP = {
    "es-ES": "es",
    "en-US": "en",
    "en-es": "es",
    "en-us": "en",
}
logger = logging.getLogger(__name__)


def _channel_img(channel_info: dict) -> str:
    image = channel_info.get("image", None)
    if not image:
        image = channel_info["itunes:image"]
        return image["@href"]
    if isinstance(image, list):
        image = image[0]
    return image["url"]


def _episode_date(date: str) -> datetime:
    return dateutil.parser.parse(date)


def _episode_duration(duration: typing.Optional[str]) -> int:
    hours, minutes, secs = "0", "0", "0"
    if not duration:
        return -1
    if ":" in duration:
        parts = duration.split(":")
        if len(parts) == 3:
            hours, minutes, secs = parts
        elif len(parts) == 2:
            minutes, secs = parts
        return int(hours) * 3600 + int(minutes) * 60 + int(secs)
    return int(duration)

def _episode_filename_from_url(url: str) -> str:
    return re.match("\/([^\/]+)$", url)

def _episode_guid(guid: typing.Union[dict, str]) -> str:
    return guid["#text"] if isinstance(guid, dict) else guid


def _read_channel_feed(url: str) -> dict | None:
    try:
        channel_info = xmltodict.parse(requests.get(url).content)
    except xml.parsers.expat.ExpatError:
        channel_info = None
    return channel_info


def read_channel(url: str, language: str | None = None) -> models.Channel | None:
    """Read a feed url and return a channel object (not stored yet in
    db). This function won't read channel episodes, just some basic
    metadata about channels.
    """
    logger.info(f"reading channel from url: {url}")
    if parsed_channel := _read_channel_feed(url):
        channel_info = parsed_channel["rss"]["channel"]
        language = language or channel_info["language"].lower()
        return models.Channel(
            kind=models.ChannelKind.podcast.value,
            title=channel_info["title"],
            description=channel_info["description"],
            language=LANGUAGES_MAP.get(language, ""),
            url=channel_info["link"],
            feed=url,
            local_folder="",
            image=_channel_img(channel_info),
        )


def read_episodes(channel: models.Channel) -> list[models.Episode]:
    """Return a list with all the episodes (not stored yet in db) from
    a given channel.
    """
    logger.info(f"reading episodes from channel: {channel.id}: {channel.title}")
    feed = _read_channel_feed(channel.feed)
    episodes: list[models.Episode] = []
    for ep in feed["rss"]["channel"]["item"]:
        if ep.get("itunes:episodeType", None) not in ["bonus", "trailer"]:
            title = ep.get("title", None)
            if title:
                url=ep["enclosure"]["@url"]
                episode = models.Episode(
                    title=title,
                    filename=_episode_filename_from_url(url),
                    guid=_episode_guid(ep["guid"]),
                    description=ep.get("description", "") or "",
                    date=_episode_date(ep["pubDate"]),
                    url=url,
                    episode=int(ep.get("itunes:episode", -1)),
                    season=int(ep.get("itunes:season", -1)),
                    duration=_episode_duration(ep.get("itunes:duration", None)),
                    transcribed=False,
                    embeddings=False,
                )
                episodes.append(episode)
            else:
                logger.warning(f"episode without title: {ep} won't be stored")
    logger.info(f"{len(episodes)} episodes parsed from channel {channel.title}")
    return episodes
