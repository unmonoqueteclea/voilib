# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

"""Functions to store and retrieve information from/to the vector
database.
"""

from typing import Optional, Union
import pathlib
import qdrant_client
from qdrant_client import models
import sentence_transformers
from voilib import embedding
from voilib.models import Episode
import uuid
from functools import cache
from typing import NamedTuple

DEFAULT_COLLECTION: str = "vectordb"


class QueryResponse(NamedTuple):
    score: float
    episode: int
    channel: int
    start_secs: int
    end_secs: int
    text: str


def get_client(
    host: Optional[str] = None,
    port: Optional[int] = None,
    path: Optional[Union[str, pathlib.Path]] = None,
) -> qdrant_client.QdrantClient:
    """Return vector database client, that can be connected to a
    server if host and port are given, a local model persisted in disk
    if a path is given or just in memory if no argument is provided.

    """
    if host and port:
        return qdrant_client.QdrantClient(host=host, port=port)
    elif path:
        return qdrant_client.QdrantClient(path=str(path))
    return qdrant_client.QdrantClient(":memory:")


def create_collection(
    client: qdrant_client.QdrantClient,
    name: str,
    embeddings_model: sentence_transformers.SentenceTransformer,
) -> None:
    """Create a collection in the vector database with the given name."""
    vsize = embeddings_model.get_sentence_embedding_dimension()
    client.recreate_collection(
        collection_name=name,
        vectors_config=models.VectorParams(
            size=vsize,  # type: ignore
            distance=models.Distance.COSINE,
        ),
    )


@cache
def ensure_collection(
    client: qdrant_client.QdrantClient,
    collection_name: str,
    embeddings_model: sentence_transformers.SentenceTransformer,
):
    found = [c for c in client.get_collections() if c == collection_name]
    if not found:
        create_collection(client, collection_name, embeddings_model)
    return


def _gen_metadata(fragment: embedding.Fragment, episode: Episode) -> dict:
    # additional metadata we store in the vector database for each fragment
    return {
        "episode": episode.pk,
        "channel": episode.channel.pk,  # type: ignore
        "start_secs": fragment.start_secs,
        "end_secs": fragment.end_secs,
        "text": fragment.text,
    }


async def add_episode(
    episode: Episode,
    client: qdrant_client.QdrantClient,
    embeddings: embedding.Embeddings,
    collection_name: str,
    fragments: list[embedding.Fragment],
) -> None:
    """Store the given embeddings from an episode in the vector
    database.

    """
    if episode.embeddings:
        raise ValueError(f"Episode {episode.pk} already stored in the vector db")
    client.upload_records(
        collection_name=collection_name,
        records=[
            models.Record(
                id=str(uuid.uuid4()),
                vector=emb.tolist(),
                payload=_gen_metadata(fragment, episode),
            )
            for emb, fragment in zip(embeddings, fragments)
        ],
    )
    episode.embeddings = True
    await episode.update()
    return


def search(
    client: qdrant_client.QdrantClient,
    query_embedding: embedding.Embeddings,
    collection_name: str,
    num_results: int,
) -> list[QueryResponse]:
    """Perform a query with the given vector database and embeddings."""
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding[0].tolist(),
        limit=num_results,
    )
    return [QueryResponse(score=r.score, **r.payload) for r in results]  # type: ignore
