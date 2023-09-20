# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""Perform data integrity checks, trying to fix data if possible.  It
will perform the following tasks:

- fixing episodes' "transcribed" field if they have an existing
  transcription file

"""
import argparse
import asyncio

from voilib import transcription

DONT_FIX_TRANSCRIBED = "bypass fix-transcribed task"


async def _main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--dont-fix-transcribed",
        action="store_true",
        default=False,
        help=DONT_FIX_TRANSCRIBED,
    )

    args = parser.parse_args()
    if not args.dont_fix_transcribed:
        await transcription.check_all_pending_episodes()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
