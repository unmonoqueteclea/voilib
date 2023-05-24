# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

from voilib import embedding, vector, storage, transcription


async def test_calculate_fragments(jobs_transcription, fake_episode):
    embs = embedding.calculate_fragments(jobs_transcription, 20)
    assert len(embs) == 2
    tr = transcription.read_transcription(
        await storage.transcription_file(fake_episode)
    )
    embs = embedding.calculate_fragments(tr, 20)
    assert len(embs) == 101

    embs = embedding.calculate_fragments(tr, 40)
    assert len(embs) == 54


async def test_store_embeddings(fake_episode):
    # load vector database
    embedding.load_embeddings_model(embedding.DEFAULT_EMBEDDINGS_MODEL)
    client = vector.get_client()

    # load episode and calculate its embeddings
    tr = transcription.read_transcription(
        await storage.transcription_file(fake_episode)
    )
    model = embedding.load_embeddings_model(embedding.DEFAULT_EMBEDDINGS_MODEL)
    embs, fragments = embedding._transcription_embeddings(
        tr, model, embedding.DEFAULT_FRAGMENT_WORDS
    )
    assert len(fragments) == 54
    assert len(embs) == 54
    assert embs[0].shape == (embedding.EMBEDDINGS_SIZE,)

    # store embeddings
    dbname = "test"
    vector.ensure_collection(client, dbname, model)
    vector.ensure_collection(client, dbname, model)
    await vector.add_episode(fake_episode, client, embs, dbname, fragments)

    # example query
    query = embedding.text2embedding("playing golf with other people", model)
    results = vector.search(client, query, dbname, 3)
    assert len(results) == 3
    for r in results:
        assert r.text
        assert r.score
        assert r.start_secs
        assert r.end_secs
    return
