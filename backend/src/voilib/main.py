# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Main module that will be always executed on startup.

"""
import logging

import fastapi
from fastapi.middleware import cors
from fastapi_pagination import add_pagination

import voilib
from voilib import db, routers

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

app = fastapi.FastAPI(title="voilib", version=voilib.__version__)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db.setup_database(app)

app.include_router(routers.app.router)
app.include_router(routers.users.router)
app.include_router(routers.media.router)
app.include_router(routers.analytics.router)

add_pagination(app)
