"""mod_config.py

Defines the configuration data structure for the mod,
including metadata and target Minecraft version.
"""


class ModConfig:
	"""Holds mod metadata and configuration."""

	VALID_MC_VERSIONS = [
		# 1.14.x
		"1.14",
		"1.14.1",
		"1.14.2",
		"1.14.3",
		"1.14.4",
		# 1.15.x
		"1.15",
		"1.15.1",
		"1.15.2",
		# 1.16.x
		"1.16",
		"1.16.1",
		"1.16.2",
		"1.16.3",
		"1.16.4",
		"1.16.5",
		# 1.17.x
		"1.17",
		"1.17.1",
		# 1.18.x
		"1.18",
		"1.18.1",
		"1.18.2",
		# 1.19.x
		"1.19",
		"1.19.1",
		"1.19.2",
		"1.19.3",
		"1.19.4",
		# 1.20.x
		"1.20",
		"1.20.1",
		"1.20.2",
		"1.20.3",
		"1.20.4",
		"1.20.5",
		"1.20.6",
		# 1.21.x
		"1.21",
		"1.21.1",
		"1.21.2",
		"1.21.3",
		"1.21.4",
	]

	FABRIC_API_VERSIONS = {
		"1.14": "0.2.7+build.127",
		"1.14.1": "0.3.0+build.200",
		"1.14.2": "0.3.0+build.207",
		"1.14.3": "0.3.0+build.208",
		"1.14.4": "0.3.0+build.209",
		"1.15": "0.4.0+build.240",
		"1.15.1": "0.4.1+build.245",
		"1.15.2": "0.4.2+build.246",
		"1.16": "0.9.0+build.203",
		"1.16.1": "0.9.1+build.205",
		"1.16.2": "0.10.0+build.208",
		"1.16.3": "0.10.1+build.209",
		"1.16.4": "0.10.2+build.210",
		"1.16.5": "0.11.0+build.214",
		"1.17": "0.34.0+1.17",
		"1.17.1": "0.37.0+1.17",
		"1.18": "0.42.0+1.18",
		"1.18.1": "0.43.1+1.18",
		"1.18.2": "0.45.0+1.18.2",
		"1.19": "0.55.0+1.19",
		"1.19.1": "0.56.0+1.19.1",
		"1.19.2": "0.57.0+1.19.2",
		"1.19.3": "0.60.0+1.19.3",
		"1.19.4": "0.62.0+1.19.4",
		"1.20": "0.70.0+1.20",
		"1.20.1": "0.71.0+1.20.1",
		"1.20.2": "0.72.0+1.20.2",
		"1.20.3": "0.73.0+1.20.3",
		"1.20.4": "0.74.0+1.20.4",
		"1.20.5": "0.75.0+1.20.5",
		"1.20.6": "0.76.0+1.20.6",
		"1.21": "0.80.0+1.21",
		"1.21.1": "0.81.0+1.21.1",
		"1.21.2": "0.82.0+1.21.2",
		"1.21.3": "0.83.0+1.21.3",
		"1.21.4": "0.84.0+1.21.4",
	}

	FABRIC_LOOM_VERSIONS = {
		"1.14": "0.2.1",
		"1.14.1": "0.2.2",
		"1.14.2": "0.2.3",
		"1.14.3": "0.2.4",
		"1.14.4": "0.2.5",
		"1.15": "0.2.6",
		"1.15.1": "0.2.7",
		"1.15.2": "0.2.8",
		"1.16": "0.5.0",
		"1.16.1": "0.5.1",
		"1.16.2": "0.5.2",
		"1.16.3": "0.5.3",
		"1.16.4": "0.5.4",
		"1.16.5": "0.6.0",
		"1.17": "0.7.0",
		"1.17.1": "0.7.1",
		"1.18": "0.8.0",
		"1.18.1": "0.8.1",
		"1.18.2": "0.8.2",
		"1.19": "0.10.0",
		"1.19.1": "0.10.1",
		"1.19.2": "0.10.2",
		"1.19.3": "0.11.0",
		"1.19.4": "0.11.1",
		"1.20": "0.12.0",
		"1.20.1": "0.12.1",
		"1.20.2": "0.12.2",
		"1.20.3": "0.12.3",
		"1.20.4": "0.12.4",
		"1.20.5": "0.12.5",
		"1.20.6": "0.12.6",
		"1.21": "0.13.0",
		"1.21.1": "0.13.1",
		"1.21.2": "0.13.2",
		"1.21.3": "0.13.3",
		"1.21.4": "0.13.4",
	}

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

	def get_fabric_api_version(self):
		"""Get the appropriate Fabric API version for the configured MC version."""
		return self.FABRIC_API_VERSIONS[self.mc_version]

	def get_fabric_loom_version(self):
		"""Get the appropriate Fabric Loom version for the configured MC version."""
		return self.FABRIC_LOOM_VERSIONS[self.mc_version]
