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
		"1.14": "0.3.0+build.188",
		"1.14.1": "0.3.0+build.192",
		"1.14.2": "0.3.0+build.198",
		"1.14.3": "0.3.1+build.208",
		"1.14.4": "0.3.2+build.233",
		"1.15": "0.4.2+build.246",
		"1.15.1": "0.4.3+build.247",
		"1.15.2": "0.4.25+build.282",
		"1.16": "0.11.6+build.355-1.16",
		"1.16.1": "0.16.3+build.390-1.16.1",
		"1.16.2": "0.21.1+build.329-1.16",
		"1.16.3": "0.25.7+build.380-1.16",
		"1.16.4": "0.33.1+build.318-1.16",
		"1.16.5": "0.42.1+1.16",
		"1.17": "0.47.9+1.17",
		"1.17.1": "0.52.4+1.17",
		"1.18": "0.58.0+1.18.2",
		"1.18.1": "0.61.0+1.18.1",
		"1.18.2": "0.65.2+1.18.2",
		"1.19": "0.70.0+1.19",
		"1.19.1": "0.72.1+1.19.1",
		"1.19.2": "0.76.1+1.19.2",
		"1.19.3": "0.80.1+1.19.3",
		"1.19.4": "0.84.0+1.19.4",
		"1.20": "0.88.1+1.20",
		"1.20.1": "0.90.4+1.20.1",
		"1.20.2": "0.92.0+1.20.2",
		"1.20.3": "0.93.2+1.20.3",
		"1.20.4": "0.96.5+1.20.4",
		"1.20.5": "0.98.2+1.20.5",
		"1.20.6": "0.99.4+1.20.6",
		"1.21": "0.100.3+1.21",
		"1.21.1": "0.103.0+1.21.1",
		"1.21.2": "0.106.1+1.21.2",
		"1.21.3": "0.108.0+1.21.3",
		"1.21.4": "0.112.2+1.21.4",
	}

	FABRIC_LOOM_VERSIONS = {
		"1.14": "0.10.66",
		"1.14.1": "0.10.66",
		"1.14.2": "0.10.66",
		"1.14.3": "0.10.66",
		"1.14.4": "0.10.66",
		"1.15": "0.11.34",
		"1.15.1": "0.11.34",
		"1.15.2": "0.11.34",
		"1.16": "0.12.56",
		"1.16.1": "0.12.56",
		"1.16.2": "0.12.56",
		"1.16.3": "0.12.56",
		"1.16.4": "0.12.56",
		"1.16.5": "0.12.56",
		"1.17": "1.0.18",
		"1.17.1": "1.0.18",
		"1.18": "1.1.14",
		"1.18.1": "1.1.14",
		"1.18.2": "1.1.14",
		"1.19": "1.2.8",
		"1.19.1": "1.2.8",
		"1.19.2": "1.2.8",
		"1.19.3": "1.2.8",
		"1.19.4": "1.2.8",
		"1.20": "1.3.10",
		"1.20.1": "1.3.10",
		"1.20.2": "1.4.6",
		"1.20.3": "1.4.6",
		"1.20.4": "1.4.6",
		"1.20.5": "1.5.8",
		"1.20.6": "1.5.8",
		"1.21": "1.6.12",
		"1.21.1": "1.6.12",
		"1.21.2": "1.7.4",
		"1.21.3": "1.7.4",
		"1.21.4": "1.8.13",
	}

	JAVA_REQUIREMENTS = [
		# Tuple format: (mc_version, min_java_version, recommended_java_version)
		("1.21.4", 21, 21),  # Java 17+ required
		("1.20.4", 17, 17),  # Java 17+ required
		("1.18", 17, 17),  # Java 17+ required
		("1.17", 16, 16),  # Java 16+ required
		("1.14", 8, 8),  # Java 8+ required
	]

	def __init__(
		self,
		mod_name: str,
		mod_id: str,
		version: str = "1.0.0",
		description: str = "",
		mc_version: str = "1.19.2",
		authors: list = None,
		group: str = None,
		contact: dict = None,
	):
		"""Initialize the mod config.

		:param mod_name: Name of the mod (e.g. "My Awesome Mod")
		:param mod_id:   Unique ID of the mod (no spaces, e.g. "myawesomemod")
		:param version:  Version of the mod
		:param description: A short description
		:param mc_version: The target Minecraft version (e.g. "1.19.2")
		:param authors: List of mod authors
		:param group: Maven group ID (defaults to mod_id)
		:param contact: Dictionary with contact info (e.g. {"homepage": "..."})
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
		self.authors = authors or [mod_name]
		self.group = group or mod_id
		self.contact = contact or {"homepage": f"https://github.com/user/{mod_id}"}

	def __repr__(self):
		return (
			f"ModConfig(mod_name={self.mod_name}, mod_id={self.mod_id}, "
			f"version={self.version}, description={self.description}, "
			f"mc_version={self.mc_version}, authors={self.authors}, "
			f"group={self.group}, contact={self.contact})"
		)

	def get_fabric_api_version(self):
		"""Get the appropriate Fabric API version for the configured MC version."""
		return self.FABRIC_API_VERSIONS[self.mc_version]

	def get_fabric_loom_version(self):
		"""Get the appropriate Fabric Loom version for the configured MC version."""
		# Use a more modern version of Fabric Loom that's compatible with newer Java versions
		return self.FABRIC_LOOM_VERSIONS[self.mc_version]

	def get_required_java_version(self):
		"""Get the minimum required Java version for this MC version."""
		for mc_ver, min_java, rec_java in self.JAVA_REQUIREMENTS:
			if self._version_matches_or_newer(self.mc_version, mc_ver):
				return min_java, rec_java
		return 8, 8  # Default to Java 8 for very old versions

	def _version_matches_or_newer(self, version, target):
		"""Helper to compare Minecraft versions."""
		v1 = [int(x) for x in version.split(".")]
		v2 = [int(x) for x in target.split(".")]
		# Pad versions to same length
		while len(v1) < len(v2):
			v1.append(0)
		while len(v2) < len(v1):
			v2.append(0)
		return v1 >= v2
