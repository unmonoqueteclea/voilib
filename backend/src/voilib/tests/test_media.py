# Copyright (c) 2022 Pablo González Carrizo
# All rights reserved.


def test_crud_episodes(channel, auth_client) -> None:  # type: ignore
    # list all episodes
    response = auth_client.get("/media/episode").json()
    assert response["total"] > 0
    assert response["items"][0]["id"]
    assert response["items"][0]["title"]


def test_crud_channels(channel, auth_client) -> None:  # type: ignore
    # list all channels
    response = auth_client.get("/media/channel").json()
    assert response["total"] == 1
    assert len(response["items"]) > 0
    assert response["items"][0]["id"]
    assert response["items"][0]["title"]
    assert response["items"][0]["image"]
    # filter channels by title
    title = channel.title
    response = auth_client.get(
        f"/media/channel?title__icontains={title[:10]}"
    ).json()
    assert response["total"] == 1
    cid = response["items"][0]["id"]
    assert "pk" not in response["items"][0]
    # get channel by its id
    response = auth_client.get(f"/media/channel/{cid}").json()
    assert response["id"] == cid
    # delete channel by its id
    response = auth_client.delete(f"/media/channel/{cid}").json()
    assert response["deleted_rows"] == 1
    response = auth_client.get("/media/channel").json()
    assert response["total"] == 0
    # create a new channel
    data = {"feed_url": channel.feed}
    response = auth_client.post("/media/channel", json=data).json()
    assert response["id"]
    assert title in response["title"]
    assert "pk" not in response
