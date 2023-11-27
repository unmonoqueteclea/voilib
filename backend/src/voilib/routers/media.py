# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

import logging
import uuid
from typing import Optional

import fastapi
from fastapi_pagination import Page
from fastapi_pagination.ext.ormar import paginate
from voilib import auth, storage, tasks, transcription
from voilib.collection import crawler
from voilib.models import analytics, media, users
from voilib.schemas import media as media_schemas

logger = logging.getLogger(__name__)
router = fastapi.APIRouter(prefix="/media", tags=["media"])


async def store_user_query(query_text: str) -> analytics.Query:
    """Store query performed by a user"""
    query = analytics.Query(text=query_text)
    await query.save()
    return query


@router.get(
    "/channel",
    summary="Get the paginated list of channels in the database",
    response_model=Page[media_schemas.ChannelOut],  # type: ignore
)
async def channels(  # type: ignore
    pk: Optional[int] = None,
    title__icontains: Optional[str] = None,
    description__icontains: Optional[str] = None,
):
    qs = media.Channel.objects
    if pk:
        qs = qs.filter(pk=pk)
    if title__icontains:
        qs = qs.filter(title__icontains=title__icontains)
    if description__icontains:
        qs = qs.filter(description__icontains=description__icontains)
    return await paginate(qs)


@router.get(
    "/channel/{channel_id}",
    summary="Get a single channel by its ids",
    response_model=media_schemas.ChannelOut,
)
async def get_channel(
    channel_id: uuid.UUID,
    admin: users.User = fastapi.Depends(auth.get_current_admin_user),
) -> media_schemas.ChannelOut:  # type: ignore
    channel = await media.Channel.objects.get(id=channel_id)
    return channel


@router.post(
    "/channel",
    summary="Add a new channel from its feed url, or return it if it exits",
    response_model=media_schemas.ChannelOut,
)
async def add_channel(
    channel_in: media_schemas.ChannelIn = fastapi.Body(...),
    admin: users.User = fastapi.Depends(auth.get_current_admin_user),
) -> media_schemas.ChannelOut:  # type: ignore
    _, channel = await crawler.get_or_create_channel(channel_in.feed_url)
    return channel


@router.delete("/channel/{channel_id}", summary="Delete a channel given its id")
async def delete_channel(
    channel_id: uuid.UUID,
    admin: users.User = fastapi.Depends(auth.get_current_admin_user),
) -> dict:
    channel = await media.Channel.objects.get(id=channel_id)
    return {"deleted_rows": await channel.delete()}


@router.get(
    "/episode",
    summary="Get the paginated list of episodes",
    response_model=Page[media_schemas.EpisodeOut],  # type: ignore
)  # type: ignore
async def episodes(
    pk: Optional[int] = None,
    channel: Optional[uuid.UUID] = None,
    transcribed: Optional[bool] = None,
    embeddings: Optional[bool] = None,
    title__icontains: Optional[str] = None,
    description__icontains: Optional[str] = None,
    admin: users.User = fastapi.Depends(auth.get_current_admin_user),
):
    """Return a list with all the available episodes."""
    qs = media.Episode.objects
    if pk:
        qs = qs.filter(pk=pk)
    if transcribed is not None:
        qs = qs.filter(transcribed=transcribed)
    if embeddings is not None:
        qs = qs.filter(embeddings=embeddings)
    if channel:
        qs = qs.filter(channel__id=channel)
    if title__icontains:
        qs = qs.filter(title__icontains=title__icontains)
    if description__icontains:
        qs = qs.filter(description__icontains=description__icontains)
    return await paginate(qs)


@router.get(
    "/episode/{episode_id}/transcription",
    summary="Get the transcription of a single episode by its id",
    response_model=media_schemas.Transcription,
)
async def get_episode_transcription(
    episode_id: uuid.UUID, limit: int = 100, offset: int = 0
) -> media_schemas.Transcription:  # type: ignore
    episode = await media.Episode.objects.get(id=episode_id)
    tr = transcription.read_transcription(await storage.transcription_file(episode))
    return media_schemas.Transcription(
        count=len(tr), offset=offset, transcription=tr[offset : offset + limit]
    )


@router.delete("/episode/{episode_id}", summary="Delete an episode given its id")
async def delete_episode(
    episode_id: uuid.UUID,
    admin: users.User = fastapi.Depends(auth.get_current_admin_user),
) -> dict:
    episode = await media.Episode.objects.get(id=episode_id)
    return {"deleted_rows": await episode.delete()}


@router.get(
    "/query",
    summary="Perform a new query in the whole database",
    response_model=list[media_schemas.QueryResponse],
)
async def query(
    query_text: str,
    background_tasks: fastapi.BackgroundTasks,
    k: int = 6,
):
    background_tasks.add_task(store_user_query, query_text)
    output: list[media_schemas.QueryResponse] = []
    for r in tasks.search(query_text, k):
        episode = await media.Episode.objects.get(pk=r.episode)
        output.append(
            media_schemas.QueryResponse(
                text=r.text,
                episode=episode,
                channel=await episode.channel.load(),  # type: ignore
                similarity=r.score,
                start=r.start_secs,
            )
        )
    return output
