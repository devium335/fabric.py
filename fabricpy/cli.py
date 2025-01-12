"""cli.py

Command-line interface for fabricpy.
"""

import argparse
import os
import sys

from fabricpy.block import Block
from fabricpy.generator import generate_mod_project
from fabricpy.item import Item
from fabricpy.mod_config import ModConfig

# If you want to compile using Gradle, you could also do:
# from fabricpy.utils import run_command


def main():
	parser = argparse.ArgumentParser(
		prog="fabricpy",
		description="CLI for fabricpy: Generate and compile Fabric mods in Python.",
	)

	subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

	# Subcommand: compile
	compile_parser = subparsers.add_parser(
		"compile",
		help="Generate (and optionally build) the Fabric mod project.",
	)
	compile_parser.add_argument(
		"config_script",
		type=str,
		help="Path to a Python script defining mod_config, blocks, items lists.",
	)
	compile_parser.add_argument(
		"-o",
		"--output",
		type=str,
		default="build_mod",
		help="Output directory for the generated mod project.",
	)
	compile_parser.add_argument(
		"--build",
		action="store_true",
		help="If provided, will attempt to run Gradle build after generation.",
	)

	args = parser.parse_args()

	if args.subcommand == "compile":
		_handle_compile(args)
	else:
		parser.print_help()


def _handle_compile(args):
	# 1. Execute the config script in a restricted namespace
	#    The script should define:
	#      mod_config = ModConfig(...)
	#      blocks = [Block(...), ...]
	#      items = [Item(...), ...]
	config_globals = {}
	config_locals = {}
	with open(args.config_script, encoding="utf-8") as f:
		code = f.read()

	# We'll exec the code in a dict that has references to our classes
	scope = {"ModConfig": ModConfig, "Block": Block, "Item": Item}
	exec(code, scope, scope)

	if "mod_config" not in scope or "blocks" not in scope or "items" not in scope:
		print(
			"Error: config_script must define 'mod_config', 'blocks', and 'items'.",
			file=sys.stderr,
		)
		sys.exit(1)

	mod_config = scope["mod_config"]
	blocks = scope["blocks"]
	items = scope["items"]

	# 2. Generate the mod project
	output_dir = os.path.abspath(args.output)
	generate_mod_project(mod_config, blocks, items, output_dir)

	# 3. Optionally run Gradle build
	if args.build:
		gradlew_path = os.path.join(output_dir, "gradlew")
		if not os.path.isfile(gradlew_path):
			# Minimal approach: we assume user has Gradle installed or they add
			# a wrapper themselves. For demonstration, just try `gradle build`.
			# from fabricpy.utils import run_command
			print("Attempting to build using system Gradle...")
			# run_command("gradle build", cwd=output_dir)
			print(
				"Build step is placeholder here. In a real setup, you'd run Gradle or gradlew.",
			)
		else:
			print("Found gradlew. Running './gradlew build' ...")
			# run_command("./gradlew build", cwd=output_dir)
			print(
				"Build step is placeholder here. In a real setup, you'd run Gradle or gradlew.",
			)
