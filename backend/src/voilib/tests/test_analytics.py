# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

from voilib.routers import media


async def test_queries(auth_client):
    for i in range(100):
        await media.store_user_query(f"User searched for {i}")
    response = auth_client.get("/analytics/query-history?page=1&size=21").json()
    assert response["total"] == 100
    assert len(response["items"]) == 21
