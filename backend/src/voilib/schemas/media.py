# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

""" Media-related schemas.

"""
from pydantic import BaseModel
import typing
from voilib.models.base import CoreModel
from voilib.models.media import Channel, Episode

ChannelOut = Channel.get_pydantic(exclude={"pk", "episodes"})


class ChannelIn(BaseModel):
    """Information needed to create a new channel"""

    feed_url: str


EpisodeIn = Episode.get_pydantic(exclude=set(CoreModel.__fields__.keys()))
EpisodeOut = Episode.get_pydantic(exclude={"pk", "channel"})


class QueryResponse(BaseModel):
    """Response to a query"""

    text: str
    similarity: float
    episode: typing.Union[EpisodeOut, None]  # type: ignore
    channel: typing.Union[ChannelOut, None]  # type: ignore
    start: float
