# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

from voilib import collection


def test_default_channels() -> None:
    channels = collection.default_channels()
    assert len(channels) > 0
    for ch in channels[-5:]:
        channel = collection.read_channel(ch["url"])
        episodes = collection.read_episodes(channel)
        assert len(episodes) > 0


async def test_read_channel_and_its_episodes() -> None:
    for i, podcast in enumerate(collection.default_channels()[:5]):
        created, retrieved = await collection.get_or_create_channel(podcast["url"])
        assert created
        assert retrieved.kind == "podcast"
        created, retrieved = await collection.get_or_create_channel(podcast["url"])
        assert not created
        for f in [
            retrieved.title,
            retrieved.description,
            retrieved.url,
            retrieved.feed,
            retrieved.image,
        ]:
            assert len(f) > 0
        if i == 0:
            assert (await collection.update_channel(retrieved)) > 0
            assert (await collection.update_channel(retrieved)) == 0
