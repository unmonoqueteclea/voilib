# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

"""User-related endpoints

"""

import logging
import re
from datetime import timedelta
import fastapi.security
import fastapi

from voilib import auth, settings
from voilib.models import users
from voilib.schemas import users as user_schemas

logger = logging.getLogger(__name__)
router = fastapi.APIRouter(prefix="/users", tags=["users"])

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
MIN_PWD_LENGTH = 8


@router.post(
    "/signup",
    summary="Create new app user. Username and email are unique",
    response_model=user_schemas.UserOut,
)
async def signup(
    user_info: user_schemas.SignUpUserIn = fastapi.Body(...),
) -> users.User:
    user = await auth.get_user(user_info.username)
    user_by_email = await auth.get_user_by_email(user_info.email)
    if user is not None or user_by_email is not None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exist",
        )
    if not re.match(EMAIL_REGEX, user_info.email):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Email is not correct",
        )
    if len(user_info.password) < MIN_PWD_LENGTH:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Password too short. At least {MIN_PWD_LENGTH} required",
        )
    return await users.User.objects.create(
        email=user_info.email,
        username=user_info.username,
        hashed_password=auth.get_password_hash(user_info.password),
        admin=user_info.username == settings.settings.admin_username,
    )


@router.post(
    "/token",
    summary="Login user and obtain access token",
    response_model=user_schemas.Token,
)
async def login_for_access_token(
    form_data: fastapi.security.OAuth2PasswordRequestForm = fastapi.Depends(),
) -> dict:
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": auth.create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        "token_type": "bearer",
    }


@router.get(
    "/me",
    summary="Get currently logged user",
    response_model=user_schemas.UserOut,
)
async def read_users_me(
    current_user: users.User = fastapi.Depends(auth.get_current_user),
) -> users.User:
    return current_user
