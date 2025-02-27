"""Top-level package for omemetools."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """OmemeTools"""
__email__ = "omemeankohji@gmail.com"
__version__ = "0.0.1"

from .src.AsunaroTools.nodes import NODE_CLASS_MAPPINGS
from .src.AsunaroTools.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
