"""utils.py

Utility functions that might be used throughout the library.
"""

import subprocess


def run_command(command: str, cwd: str = None):
	"""Runs a shell command in a subprocess."""
	print(f"Running command: {command}")
	try:
		subprocess.check_call(command, shell=True, cwd=cwd)
	except subprocess.CalledProcessError as e:
		raise RuntimeError(f"Command failed: {command}\n{e!s}")
