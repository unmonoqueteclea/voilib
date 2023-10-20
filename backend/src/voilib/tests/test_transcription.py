# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

import pytest
from voilib import transcription


@pytest.mark.skip(reason="not reliable between different versions")
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

    original_text = "".join([r[2] for r in jobs_transcription])
    current_text = "".join([r[2] for r in read])

    assert original_text == current_text
