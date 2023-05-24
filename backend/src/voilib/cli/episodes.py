# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Perform episode-related tasks

Some of them need a running Redis and RQ worker.

"""
import argparse
import asyncio
import logging
from voilib import collection, tasks

logger = logging.getLogger(__name__)


async def _main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--add-default-channels",
        action="store_true",
        default=False,
        help="Add all default channels hardcoded in the codebase",
    )

    parser.add_argument(
        "--update",
        action="store_true",
        default=False,
        help="Update all channels from their feeds",
    )

    parser.add_argument(
        "--transcribe-days",
        action="store",
        type=int,
        default=-1,
        help="Transcribe pending episodes from this amount of days",
    )

    parser.add_argument(
        "--store",
        action="store_true",
        default=False,
        help="Store pending episodes in the vector database",
    )

    args = parser.parse_args()
    if args.add_default_channels:
        logger.info("adding default channels form an background task")
        await collection.add_default_channels()
    if args.update:
        logger.info("updating channels form an background task")
        await tasks.update_channels()
    if args.transcribe_days > 0:
        await tasks.transcribe_episodes(args.transcribe_days)
    if args.store:
        await tasks.store_episodes_embeddings()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
