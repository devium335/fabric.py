"""block.py

Defines a representation of a block in Minecraft.
"""


class Block:
	"""Represents a custom block to be added to the mod."""

	def __init__(
		self,
		block_id: str,
		name: str,
		texture_file: str = "block.png",
		category: str = "misc",
	):
		"""Initialize a new block.

		:param block_id: Unique ID of the block (e.g. "my_block")
		:param name: Readable name (e.g. "My Block")
		:param texture_file: Path or filename of the block's texture (PNG)
		:param category: A category (e.g. "building_blocks", "misc", etc.)
		                 or any custom category name
		"""
		self.block_id = block_id
		self.name = name
		self.texture_file = texture_file
		self.category = category

	def __repr__(self):
		return (
			f"Block(block_id={self.block_id}, name={self.name}, "
			f"texture_file={self.texture_file}, category={self.category})"
		)
