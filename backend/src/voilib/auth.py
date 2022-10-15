# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

"""Authentication and security stuff

We are using JWT tokens as the main authorization method in the API.

The global variable ACCESS_TOKEN_EXPIRE_MINUTES control the access
token expiration time.

"""

from datetime import datetime, timedelta
from typing import Optional
import fastapi
from fastapi import security
from jose import JWTError, jwt
from passlib import context

from voilib import models
from voilib.settings import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="users/token")
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str) -> Optional[models.User]:
    """Return (asynchronously) a user by its username or None if it
    doesn't exist.

    """
    return await models.User.objects.get_or_none(username=username)


async def get_user_by_email(email: str) -> Optional[models.User]:
    """Return (asynchronously) a user by its email or None if it
    doesn't exist.

    """
    return await models.User.objects.get_or_none(email=email)


def get_password_hash(password: str) -> str:
    """Return the hash for a given password"""
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> Optional[models.User]:
    """Authenticate (asynchronously) a user by its username and
    password and password.

    It will return the user if the authentication succeed or None
    otherwise.

    """
    user = await get_user(username)
    if user and _verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Return an access token with the given data and expiration time
    delta (default ACCESS_TOKEN_EXPIRE_MINUTES)
    """
    to_encode = data.copy()
    delta = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": datetime.utcnow() + delta})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


async def get_current_user(
    token: str = fastapi.Depends(oauth2_scheme),
) -> models.User:
    """Function to get current user by reading access token.
    The username is stored in the token.
    Use it with fastapi.Depends

    If the token is not correct, it will return generate a 401 code.
    """
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub") if payload else None
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin_user(
    current_user: models.User = fastapi.Depends(get_current_user),
) -> models.User:
    """Function to get current admin user by reading access token.  It
    is the same as get_current_user but it also checks it the user is
    an admin.  Use it with fastapi.Depends

    If the user is not an admin (or the token is not correct) it will
    generate a 401 code.

    """
    if not current_user.admin:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="User is not an admin",
        )

    return current_user
