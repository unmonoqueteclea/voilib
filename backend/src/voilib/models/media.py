# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Media-related models. The main two media entities are Episode (a
specific media item, a podcast episode) and Channel (a collection of
related episodes).

"""
import enum
from typing import Optional

import ormar
from voilib.models import base


class ChannelKind(enum.Enum):
    podcast = "podcast"
    local = "local"


class Language(enum.Enum):
    es = "es"
    en = "en"
    unknown = ""


class Channel(base.CoreModel):
    """A collection of related episodes. Table channels
    The field feed (that contains the feed url) is unique.
    """

    class Meta(ormar.ModelMeta):
        tablename = "channels"
        constraints = [ormar.UniqueColumns("feed")]

    title: str = ormar.String(max_length=250)  # type: ignore
    feed: str = ormar.String(max_length=250)  # type: ignore
    kind = ormar.String(max_length=10, choices=list(ChannelKind))
    language = ormar.String(max_length=3, choices=list(Language))
    description = ormar.Text()
    url: str = ormar.String(max_length=250)  # type: ignore
    local_folder: str = ormar.String(max_length=250)  # type: ignore
    image: str = ormar.String(max_length=500)  # type: ignore


class Episode(base.CoreModel):
    """A specific media item, usually a podcast episode.
    DB table episodes. Table episodes

    An episode always belongs to a Channel. If the channel is removed,
    all its episodes will be automatically removed too.

    The field fieield is unique.
    """

    class Meta(ormar.ModelMeta):
        tablename = "episodes"
        constraints = [ormar.UniqueColumns("url")]

    channel: Optional[Channel] = ormar.ForeignKey(
        Channel,
        related_name="episodes",
        ondelete=ormar.ReferentialAction.CASCADE,
    )
    title: str = ormar.String(max_length=250)  # type: ignore
    filename: str = ormar.String(max_length=250) # type: ignore
    description: str = ormar.Text()  # type: ignore
    date = ormar.DateTime(timezone=True, nullable=True)
    guid = ormar.Text()  # episode guid at origin
    url: str = ormar.Text()  # type: ignore
    episode = ormar.Integer(default=-1)
    season = ormar.Integer(default=-1)
    duration = ormar.Integer(default=-1)
    # whether transcriptions are available for the episode
    transcribed = ormar.Boolean(default=False)
    # whether embeddings are available for the episode
    embeddings = ormar.Boolean(default=False)
