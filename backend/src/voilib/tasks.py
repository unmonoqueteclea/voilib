# Copyright (c) 2023 Pablo González Carrizo
# All rights reserved.

"""Main voilib data tasks
"""

import logging
from voilib import (
    models,
    settings,
    transcription,
    collection,
    embedding,
    vector,
    storage,
)
from datetime import datetime, timedelta
import random
import sentence_transformers
import qdrant_client

logger = logging.getLogger(__name__)


async def update_channels() -> int:
    """Read feeds from all the channels in the db and update their
    episodes. Return the number of new episodes added.

    """
    logger.info("updating all channels")
    total = 0
    for ch in await models.Channel.objects.all():
        logger.info(f"updating channel {ch.id}: {ch.title}")
        added = await collection.update_channel(ch)
        logger.info(f"new episodes added to {ch.title}: {added}")
        total += added
    logger.info(f"finished channels update after creating {total}")
    return total


async def transcribe_episodes(num_days: int) -> int:
    """Transcribe episodes, in a random order, from the last num_days
    days. Return the total number of episodes transcribed.

    """
    logger.info(f"transcribing episodes from last {num_days} days")
    qs = models.Episode.objects.filter(
        transcribed=False, date__gt=datetime.now() - timedelta(days=num_days)
    )
    episodes = await qs.all()
    total = len(episodes)
    logger.info(f"{total} episodes are going to be transcribed in an async task")
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
    logger.info(f"storing embeddings for episode {episode.id}")
    embeddings, fragments = await embedding.episode_embeddings(
        episode, model, embedding.DEFAULT_FRAGMENT_WORDS
    )
    await vector.add_episode(episode, client, embeddings, collection_name, fragments)
    return


async def store_episodes_embeddings() -> None:
    """Store pending episodes embeddings in the vector database"""
    logger.info("storing all pending episodes in vector database")
    client = vector.get_client(path=str(storage.vectordb_path()))
    model = embedding.load_embeddings_model(embedding.DEFAULT_EMBEDDINGS_MODEL)
    vector.ensure_collection(client, vector.DEFAULT_COLLECTION, model)
    episodes = await models.Episode.objects.filter(
        transcribed=True, embeddings=False
    ).all()
    random.shuffle(episodes)
    for episode in episodes:
        await store_episode_embeddings(
            episode, model, client, vector.DEFAULT_COLLECTION
        )
    return


def search(text: str) -> list[vector.QueryResponse]:
    model = embedding.load_embeddings_model(embedding.DEFAULT_EMBEDDINGS_MODEL)
    client = vector.get_client(path=str(storage.vectordb_path()))
    query = embedding.text2embedding(text, model)
    results = vector.search(client, query, vector.DEFAULT_COLLECTION, 8)
    return results
