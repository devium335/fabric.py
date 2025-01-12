"""item.py

Defines a representation of an item in Minecraft.
"""


class Item:
	"""Represents a custom item to be added to the mod."""

	def __init__(
		self,
		item_id: str,
		name: str,
		texture_file: str = "item.png",
		category: str = "misc",
	):
		"""Initialize a new item.

		:param item_id: Unique ID of the item (e.g. "my_item")
		:param name: Readable name (e.g. "My Item")
		:param texture_file: Path or filename of the item's texture (PNG)
		:param category: A category (e.g. "misc", "tools", etc.)
		                 or any custom category name
		"""
		self.item_id = item_id
		self.name = name
		self.texture_file = texture_file
		self.category = category

	def __repr__(self):
		return (
			f"Item(item_id={self.item_id}, name={self.name}, "
			f"texture_file={self.texture_file}, category={self.category})"
		)
