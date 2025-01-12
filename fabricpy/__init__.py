"""fabricpy
========
A Python-based library to generate Fabric Minecraft mods.
"""

__version__ = "0.1.0-alpha"

# Re-export classes for easier import
from .block import Block
from .item import Item
from .mod_config import ModConfig

__all__ = ["Block", "Item", "ModConfig"]
