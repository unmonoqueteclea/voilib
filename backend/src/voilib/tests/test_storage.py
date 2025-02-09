# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

from voilib import storage


async def test_episodes(channel) -> None:  # type: ignore
    assert "kaizen" in storage.MEDIA_PATH / channel.title
    assert await channel.episodes.count() == 5
    ep = await channel.episodes.first()
    trfile = await storage.transcription_file(ep)
    assert ".csv" in str(trfile)
    epfile = storage.MEDIA_PATH / channel.title / ep.filename
    assert ".mp3" in str(epfile)
    assert trfile.stem == epfile.stem
    assert (await storage.download_episode(ep)).exists()
