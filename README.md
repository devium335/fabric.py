# fabricpy

A Python library to create (generate) Fabric Minecraft mods in Python.

## Features

-   Specify mod metadata (name, ID, version, description).
-   Select Minecraft version (1.8 through 1.21).
-   Add custom blocks and items with textures.
-   Generate a ready-to-use Fabric mod project, including Java code, Gradle build scripts, and resource files.
-   Includes a CLI for easy usage, plus Sphinx documentation for reference.

## Installation

```bash
pip install fabricpy
```

## Usage Example

1. Create a configuration script (e.g. `my_mod_config.py`) that defines:

```python
from fabricpy import ModConfig, Block, Item

mod_config = ModConfig(
    mod_name="Example Mod",
    mod_id="examplemod",
    mc_version="1.19.2"
)

blocks = [
    Block("my_block", "My Block", texture_file="my_block.png")
]

items = [
    Item("my_item", "My Item", texture_file="my_item.png")
]
```

2. Compile the mod:
```bash
fabricpy compile my_mod_config.py -o build_mod --build
```

3. A minimal Fabric mod project is generated in `build_mod/`.