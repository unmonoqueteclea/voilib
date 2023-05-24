# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Classes used as a parent for other app models.

"""
import uuid
from datetime import datetime

import ormar

from voilib.db import database, metadata


class CoreModel(ormar.Model):
    """Parent model of almost all the rest of app models. No table
    associated (abstract).

    We distinguish between the auto-incremental primary key (pk) and
    the public uuid exposed through the API (id), so both fields will
    be created.

    """

    pk = ormar.Integer(primary_key=True)
    id: uuid.UUID = ormar.UUID(default=uuid.uuid4, uuid_format="string")  # type: ignore
    created_at = ormar.DateTime(default=datetime.now, timezone=True)

    class Meta:
        abstract = True
        metadata = metadata
        database = database
