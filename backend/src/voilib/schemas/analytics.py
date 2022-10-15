# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

""" Analytics-related schemas.

"""
from pydantic import BaseModel

from voilib.models.analytics import Query

QueryOut = Query.get_pydantic(exclude={"pk"})


class ChannelAnalytics(BaseModel):
    """Schema to show some analytics about a channel."""

    title: str
    total_episodes: int
    image: str
    url: str
    available_episodes: int


class MediaAnalytics(BaseModel):
    """Schema to show some analytics about all channels"""

    total_channels: int
    channels: list[ChannelAnalytics]
