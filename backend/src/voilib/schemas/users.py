# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

""" User-related schemas.
"""

from pydantic import BaseModel

from voilib.models import users


class Token(BaseModel):
    """User's access token"""

    access_token: str
    token_type: str


class SignUpUserIn(BaseModel):
    """User information needed for sign up."""

    username: str
    email: str
    password: str


UserOut = users.User.get_pydantic(exclude={"pk", "hashed_password"})
