# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.

""" App management related endpoints

"""
import fastapi

import voilib

router = fastapi.APIRouter(prefix="/app", tags=["app"])


@router.get("/version", summary="Return application version")
async def version() -> dict:
    """Return voilib back-end version.

    It is the version of the voilib-api Python package.

    """
    return {"version": voilib.__version__}
