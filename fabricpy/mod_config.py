"""mod_config.py

Defines the configuration data structure for the mod,
including metadata and target Minecraft version.
"""


class ModConfig:
	"""Holds mod metadata and configuration."""

	VALID_MC_VERSIONS = [f"1.{i}" for i in range(8, 22)] + ["1.20", "1.21"]

	def __init__(
		self,
		mod_name: str,
		mod_id: str,
		version: str = "1.0.0",
		description: str = "",
		mc_version: str = "1.19.2",
	):
		"""Initialize the mod config.

		:param mod_name: Name of the mod (e.g. "My Awesome Mod")
		:param mod_id:   Unique ID of the mod (no spaces, e.g. "myawesomemod")
		:param version:  Version of the mod
		:param description: A short description
		:param mc_version: The target Minecraft version (e.g. "1.19.2")
		"""
		if mc_version not in self.VALID_MC_VERSIONS:
			raise ValueError(
				f"Unsupported Minecraft version: {mc_version}. "
				f"Supported versions: {self.VALID_MC_VERSIONS}",
			)

		self.mod_name = mod_name
		self.mod_id = mod_id
		self.version = version
		self.description = description
		self.mc_version = mc_version

	def __repr__(self):
		return (
			f"ModConfig(mod_name={self.mod_name}, mod_id={self.mod_id}, "
			f"version={self.version}, description={self.description}, "
			f"mc_version={self.mc_version})"
		)
