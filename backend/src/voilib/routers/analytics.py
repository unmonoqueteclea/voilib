# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

import logging

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.ormar import paginate

from voilib import auth
from voilib.models import analytics, media, users
from voilib.schemas import analytics as analytics_sc

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/query-history",
    summary="Individual user queries",
    response_model=Page[analytics_sc.QueryOut],
)
async def queries(
    admin: users.User = Depends(auth.get_current_admin_user),
):
    qs = analytics.Query.objects.order_by("-created_at")
    return await paginate(qs)


@router.get(
    "/media-count",
    summary="Analytics about number of channels and episodes in the applciation",
    response_model=analytics_sc.MediaAnalytics,
)
async def _media():
    dbchannels = await media.Channel.objects.order_by("title").all()
    channels = []
    for channel in dbchannels:
        eps = channel.episodes
        channels.append(
            analytics_sc.ChannelAnalytics(
                title=channel.title,
                image=channel.image,
                url=channel.url,
                total_episodes=await eps.count(),
                available_episodes=await eps.filter(embeddings=True).count(),
            )
        )
    return analytics_sc.MediaAnalytics(
        total_channels=len(dbchannels), channels=channels
    )
