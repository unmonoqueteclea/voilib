# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Functions to create vectors (embeddings) representing fragments of
transcriptions (fragment length is configurable).

See https://www.sbert.net/examples/applications/semantic-search/README.html

"""
import functools
import logging
import typing

import numpy as np
import sentence_transformers
import torch

from voilib import models, storage
from voilib import transcription as tr

logger = logging.getLogger(__name__)
Embeddings = typing.Union[list[torch.Tensor], np.ndarray, torch.Tensor]


DEFAULT_FRAGMENT_WORDS = 40
# see https://www.sbert.net/docs/pretrained_models.html
# TODO: I could try a multilingual model that will generate aligned
# vector spaces, i.e. similar inputs in different languages are mapped
# close in vector space.
# see https://www.sbert.net/docs/pretrained_models.html#multi-lingual-models
DEFAULT_EMBEDDINGS_MODEL = "multi-qa-MiniLM-L6-cos-v1"
EMBEDDINGS_SIZE = 384


class Fragment(typing.NamedTuple):
    """A fragment represents the minimum amount of data to be stored
    in the vector database.
    """

    start_idx: int
    end_idx: int
    start_secs: float
    end_secs: float
    text: str


@functools.cache
def load_embeddings_model(name: str) -> sentence_transformers.SentenceTransformer:
    """Load transformer model from its name.

    This function uses cache so that the first time a model is loaded
    it is cached, and later function executions will just use the
    cached instance.
    """
    logger.info(f"loading and caching transformer model {name}")
    return sentence_transformers.SentenceTransformer(name)


def calculate_fragments(
    transcription: tr.Transcription, max_fragment_words: int
) -> list[Fragment]:
    """Group all the words from the given transcription in fragments
    (the minimum unit used to create embeddings) with the configured
    max words.

    """
    fragments: list[Fragment] = []
    fragment_start_idx = None
    fragment_start_time = None
    fragment_text = ""
    for i, sentence in enumerate(transcription):
        sentence_start_time, sentence_end_time, text = sentence
        if fragment_start_time is None:
            fragment_start_time = sentence_start_time
        if fragment_start_idx is None:
            fragment_start_idx = i
        fragment_text += text
        if len(fragment_text.split(" ")) >= max_fragment_words:
            fragments.append(
                Fragment(
                    start_idx=fragment_start_idx,
                    end_idx=i,
                    start_secs=fragment_start_time,
                    end_secs=sentence_end_time,
                    text=fragment_text,
                )
            )
            # append previous fragment and start a new one
            fragment_text = ""
            fragment_start_idx, fragment_start_time = None, None
        elif i == len(transcription) - 1:
            fragments.append(
                Fragment(
                    start_idx=fragment_start_idx,
                    end_idx=i,
                    start_secs=fragment_start_time,
                    end_secs=sentence_end_time,
                    text=fragment_text,
                )
            )
    return fragments


def _transcription_embeddings(
    transcription: tr.Transcription,
    model: sentence_transformers.SentenceTransformer,
    max_fragment_words: int,
) -> tuple[Embeddings, list[Fragment]]:
    fragments = calculate_fragments(transcription, max_fragment_words)
    logger.info(f"encoding {len(fragments)} fragments...")
    embeddings = model.encode([f.text for f in fragments])
    return embeddings, fragments


def text2embedding(
    text: str, model: sentence_transformers.SentenceTransformer
) -> Embeddings:
    """Return embedding from the given text."""
    logger.info(f"encoding text: {text}")
    return model.encode([text])


async def episode_embeddings(
    episode: models.Episode,
    model: sentence_transformers.SentenceTransformer,
    max_fragment_words: int,
) -> tuple[Embeddings, list[Fragment]]:
    """Return a list of embeddings for the transcription of the given
    episode.

    """
    logger.info(f"obtaining embeddings for episode {episode.pk}: {episode.title}")
    trfile = await storage.transcription_file(episode)
    if not trfile.exists():
        assert ValueError(f"cannot find transcription for {episode.pk}")
    return _transcription_embeddings(
        tr.read_transcription(trfile), model, max_fragment_words
    )
