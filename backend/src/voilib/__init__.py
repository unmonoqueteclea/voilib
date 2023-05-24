# Copyright (c) 2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""voilib back-end and API.

This module defines the __version__ variable, obtained from package
metadata.

"""
import importlib.metadata
import logging

try:
    # __package__ allows for the case where __name__ is "__main__"
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
