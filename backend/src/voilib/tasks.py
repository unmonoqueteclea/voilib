# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Main voilib data tasks
"""

import logging
import random
from datetime import datetime, timedelta
from typing import Optional

import qdrant_client
import sentence_transformers

from voilib import collection, embedding, models, settings, transcription, vector, utils

logger = logging.getLogger(__name__)


async def update_channels() -> int:
    """Read feeds from all the channels in the db and update their
    episodes. Return the number of new episodes added.

    """
    logger.info("updating all channels")
    utils.log_event("event_update_start", "")
    total = 0
    for ch in await models.Channel.objects.all():
        ch_info = f"channel {ch.id}-{ch.title}"
        logger.info(f"updating {ch_info} ")
        try:
            added = await collection.update_channel(ch)
            logger.info(f"new episodes added to {ch_info}: {added}")
            total += added
        except Exception:
            logger.error(f"error while reading channel {ch_info}", exc_info=True)
    utils.log_event("event_update_end", "")
    logger.info(f"finished channels update after creating {total}")
    return total


async def transcribe_episodes(
    num_days: int, channel: Optional[models.Channel] = None, random_order=True
) -> int:
    """Transcribe episodes, in a random order, from the last num_days
    days. Return the total number of episodes transcribed.

    """
    channel_info = f"channel {channel.pk}: {channel.title}" if channel else ""
    logger.info(f"transcribing episodes from last {num_days} days. {channel_info}")
    qs = models.Episode.objects.filter(
        transcribed=False, date__gt=datetime.now() - timedelta(days=num_days)
    )
    if channel:
        qs = qs.filter(channel=channel)
    episodes = await qs.all()
    total = len(episodes)
    logger.info(f"{total} episodes are going to be transcribed in an async task")
    if random_order:
        random.shuffle(episodes)
    for episode in episodes:
        settings.queue.enqueue(
            transcription.transcribe_episode, episode, job_timeout="600m"
        )
    return total


async def store_episode_embeddings(
    episode: models.Episode,
    model: sentence_transformers.SentenceTransformer,
    client: qdrant_client.QdrantClient,
    collection_name: str,
) -> None:
    """Obtain embeddings for a given episode and store them in the
    vector database.
    """
    title = episode.title
    logger.info(f"storing embeddings for episode {title}: {episode.pk}")
    utils.log_event("event_store_start", title)
    embeddings, fragments = await embedding.episode_embeddings(
        episode, model, embedding.DEFAULT_FRAGMENT_WORDS
    )
    await vector.add_episode(episode, client, embeddings, collection_name, fragments)
    utils.log_event("event_store_end", title)
    return


async def store_episodes_embeddings() -> None:
    """Store pending episodes embeddings in the vector database"""
    logger.info("storing all pending episodes in vector database")
    client = vector.get_configured_client()
    model = embedding.load_embeddings_model(embedding.DEFAULT_EMBEDDINGS_MODEL)
    vector.ensure_collection(client, vector.DEFAULT_COLLECTION, model)
    episodes = await models.Episode.objects.filter(
        transcribed=True, embeddings=False
    ).all()
    logger.info(f"there are {len(episodes)} pending episodes...")
    random.shuffle(episodes)
    for episode in episodes:
        await store_episode_embeddings(
            episode, model, client, vector.DEFAULT_COLLECTION
        )
    return


def search(text: str, num_results: int) -> list[vector.QueryResponse]:
    """Main query function. Use semantic search to find content
    related to the given text in all the vector database.

    """
    model = embedding.load_embeddings_model(embedding.DEFAULT_EMBEDDINGS_MODEL)
    return vector.search(
        vector.get_configured_client(),
        embedding.text2embedding(text, model),
        vector.DEFAULT_COLLECTION,
        num_results,
    )
