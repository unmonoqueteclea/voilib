# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Authentication related models

"""

import ormar

from voilib.models.base import CoreModel


class User(CoreModel):
    """Basic information about an application user. Table user

    Fields email and username are unique.  Admin field is not
    postable, it is automatically set if a user signs up with the same
    name as the admin_username defined in app settings.

    """

    class Meta(ormar.ModelMeta):
        tablename = "user"
        constraints = [
            ormar.UniqueColumns("email"),
            ormar.UniqueColumns("username"),
        ]

    email = ormar.String(max_length=400)
    username = ormar.String(max_length=40)
    hashed_password: str = ormar.String(max_length=65)  # type: ignore
    admin: bool = ormar.Boolean(default=False)
