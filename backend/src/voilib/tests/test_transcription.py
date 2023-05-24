# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

from voilib import transcription


def test_audio_transcription(tests_data_dir, jobs_transcription):  # type: ignore
    audio = tests_data_dir / "jobs.mp3"
    tr = transcription.transcribe(audio)
    assert len(tr) > 0
    assert len(tr[0]) == 3
    assert tr[0][0] == 0.0
    assert isinstance(tr[0][1], float)
    assert isinstance(tr[0][2], str)
    transcription.store_transcription(tr, tests_data_dir / "jobs.csv")
    read = transcription.read_transcription(tests_data_dir / "jobs.csv")
    assert read == jobs_transcription
