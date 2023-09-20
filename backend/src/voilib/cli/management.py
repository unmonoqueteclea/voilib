# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Perform system managent tasks.

Run --help to see available options.
"""
import argparse
import asyncio
import logging
from voilib.models import users
from voilib import auth, settings, transcription

logger = logging.getLogger(__name__)
CREATE_DEFAULT_ADMIN_USER = "create (if not exists) the default voilib admin user"
FIX_TRANSCRIBED = """fixing episodes' transcribed field if they have
an existing transcription file"""


async def _maybe_create_admin():
    username = settings.settings.admin_username
    logger.info(f"ensuring admin {username=} is created...")
    user = await auth.get_user(username)
    if not user:
        email = settings.settings.admin_email
        logger.info("admin user not created yet, creating it....")
        logger.info(f"admin user: {email=} {username=}")
        await users.User.objects.create(
            email=email,
            username=username,
            hashed_password=auth.get_password_hash(settings.settings.admin_password),
            admin=True,
        )


async def _main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--create-admin",
        action="store_true",
        default=False,
        help=CREATE_DEFAULT_ADMIN_USER,
    )

    parser.add_argument(
        "--fix-transcribed",
        action="store_true",
        default=False,
        help=FIX_TRANSCRIBED,
    )

    args = parser.parse_args()
    if args.create_admin:
        await _maybe_create_admin()
    elif args.fix_transcribed:
        await transcription.check_all_pending_episodes()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
