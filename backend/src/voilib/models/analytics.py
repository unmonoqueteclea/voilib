# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

"""Analytics related models such us queries performed by users.

"""
import ormar

from voilib.models import base


class Query(base.CoreModel):
    """A query performed by a user. Table queries"""

    class Meta(ormar.ModelMeta):
        tablename = "queries"

    text = ormar.String(max_length=150)
