# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.


def test_version(client) -> None:
    response = client.get("/app/version/").json()
    assert len(response["version"].split(".")) == 3
    assert response["version"] != "0.0.0"
