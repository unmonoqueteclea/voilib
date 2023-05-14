# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

"""Database configuration. In this module, the events that will
connect the database on app startup and disconnect it on shutdown will
be configured.

"""

import databases
import sqlalchemy
from fastapi import FastAPI

from voilib import settings


def get_db_url() -> str:
    """Obtain the url of the running database. It will be different
    depending on the environment (development, test, production).

    """
    curset = settings.settings
    base = f"sqlite:///{str(settings.settings.data_dir)}"

    ""
    if curset.environment == settings.Environment.development.value:
        return f"{base}/db-dev.sqlite"
    elif curset.environment == settings.Environment.test.value:
        return f"{base}/db-test.sqlite"
    elif curset.environment == settings.Environment.production.value:
        return f"{base}/db-prod.sqlite"
    raise ValueError(f"invalid environment value {curset.environment}")


database = databases.Database(get_db_url())
metadata = sqlalchemy.MetaData()


def setup_database(app: FastAPI) -> None:
    """Configure database operations for different app events:
    (startup, shutdown).

    """
    app.state.database = database

    @app.on_event("startup")
    async def startup() -> None:
        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()
