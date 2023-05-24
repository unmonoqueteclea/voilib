# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

from voilib import storage


async def test_episodes(channel) -> None:  # type: ignore
    assert "kaizen" in str(storage.channel_path(channel))
    assert await channel.episodes.count() == 5
    ep = await channel.episodes.first()
    trfile = await storage.transcription_file(ep)
    assert ".csv" in str(trfile)
    epfile = await storage.episode_file(ep)
    assert ".mp3" in str(epfile)
    assert trfile.stem == epfile.stem
    assert (await storage.download_episode(ep)).exists()
