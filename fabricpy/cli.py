"""cli.py

Command-line interface for fabricpy.
"""

import argparse
import os
import subprocess
import sys
from textwrap import dedent

from fabricpy.block import Block
from fabricpy.generator import generate_mod_project
from fabricpy.item import Item
from fabricpy.mod_config import ModConfig
from fabricpy.utils import run_command

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

	# Subcommand: run
	run_parser = subparsers.add_parser(
		"run",
		help="Run Minecraft with the generated mod.",
	)
	run_parser.add_argument(
		"project_dir",
		type=str,
		help="Path to the mod project directory containing build.gradle",
	)
	run_parser.add_argument(
		"--no-setup",
		action="store_true",
		help="If provided, will skip setting up the Gradle environment.",
	)

	args = parser.parse_args()

	if args.subcommand == "compile":
		_handle_compile(args)
	elif args.subcommand == "run":
		_handle_run(args)
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

	if "mod_config" not in scope:
		print(
			"Error: config_script must define 'mod_config'.",
			file=sys.stderr,
		)
		sys.exit(1)

	mod_config = scope["mod_config"]
	blocks = scope.get("blocks", [])  # Default to empty list if not defined
	items = scope.get("items", [])  # Default to empty list if not defined

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


def _check_java_version(java_path, required_version):
	"""Helper to check if a given java path meets version requirements."""
	try:
		result = subprocess.run(
			[java_path, "-version"],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
		)
		# Java -version prints to stderr
		version_output = result.stderr
		# Extract major version number
		if "version" in version_output:
			# Convert "21.0.1" or "1.8.0" to major version number
			version_str = version_output.split('"')[1].split(".")[0]
			if "1." in version_str:
				major_version = int(version_str.split(".")[1])
			else:
				major_version = int(version_str)

			if major_version >= required_version:
				print(f"Found Java {major_version}: {version_output.splitlines()[0]}")
				return True
			else:
				print(
					f"Found Java {major_version}, but version {required_version} or newer is required"
				)
	except Exception as e:
		print(f"Warning: Error checking Java at {java_path}: {e}", file=sys.stderr)
	return False


def _handle_run(args):
	# Check if the directory exists and contains build.gradle
	project_dir = os.path.abspath(args.project_dir)
	if not os.path.isdir(project_dir):
		if os.path.isfile(project_dir):
			project_dir = os.path.dirname(project_dir)
		else:
			print(f"Error: {project_dir} is not a valid directory", file=sys.stderr)
			sys.exit(1)

	build_gradle = os.path.join(project_dir, "build.gradle")
	if not os.path.isfile(build_gradle):
		print(f"Error: No build.gradle found in {project_dir}", file=sys.stderr)
		sys.exit(1)

	# Set up environment with Java 17
	env = os.environ.copy()

	# Try to find Java 17 installation
	java_home = None

	# First get required Java version from mod config
	build_gradle = os.path.join(args.project_dir, "build.gradle")
	if not os.path.isfile(build_gradle):
		print(f"Error: No build.gradle found in {project_dir}", file=sys.stderr)
		sys.exit(1)

	# Parse MC version from build.gradle to determine Java requirements
	mc_version = "1.19.2"  # Default
	with open(build_gradle) as f:
		for line in f:
			if "minecraft" in line and ":" in line:
				mc_version = line.split(":")[2].strip().strip("\"'")
				break

	mod_config = ModConfig("temp", "temp", mc_version=mc_version)
	min_java, rec_java = mod_config.get_required_java_version()

	# Try JAVA_HOME first if it's set
	if "JAVA_HOME" in os.environ:
		java_path = os.path.join(os.environ["JAVA_HOME"], "bin", "java")
		if _check_java_version(java_path, min_java):
			java_home = os.environ["JAVA_HOME"]

	if not java_home:
		# Update paths to include both Java 17 and 21 locations
		common_paths = [
			# Java 21 paths
			"/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home",
			"/opt/homebrew/opt/openjdk@21",
			# Java 17 paths
			"/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home",
			"/opt/homebrew/opt/openjdk@17",
			# Java 16 paths
			"/Library/Java/JavaVirtualMachines/temurin-16.jdk/Contents/Home",
			"/opt/homebrew/opt/openjdk@16",
			# Java 8 paths
			"/Library/Java/JavaVirtualMachines/temurin-8.jdk/Contents/Home",
			"/opt/homebrew/opt/openjdk@8",
		]

		for path in common_paths:
			if os.path.exists(path):
				java_path = os.path.join(path, "bin", "java")
				if _check_java_version(java_path, min_java):
					java_home = path
					break

	# Set JAVA_HOME and PATH to ensure we use Java 17
	if java_home:
		env["JAVA_HOME"] = java_home
		if sys.platform == "win32":
			env["PATH"] = f"{os.path.join(java_home, 'bin')};{env.get('PATH', '')}"
		else:
			env["PATH"] = f"{os.path.join(java_home, 'bin')}:{env.get('PATH', '')}"
		print(f"Using Java from: {java_home}")

		# Verify Java is accessible
		try:
			result = subprocess.run(
				["java", "-version"],
				env=env,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True,
			)
			version_output = result.stderr
			print(f"Detected Java version: {version_output.splitlines()[0]}")
		except Exception as e:
			print(f"Warning: Error verifying Java: {e}", file=sys.stderr)
	else:
		print(
			"Warning: Could not find Java 17. Please install it and set JAVA_HOME",
			file=sys.stderr,
		)
		sys.exit(1)

	# Update Gradle setup
	if not args.no_setup:
		print("Setting up Gradle environment...")
		try:
			# Clean Fabric Loom cache if it exists
			loom_cache = os.path.expanduser("~/.gradle/caches/fabric-loom")
			if os.path.exists(loom_cache):
				print("Cleaning Fabric Loom cache...")
				import shutil

				shutil.rmtree(loom_cache)

			# Create gradle.properties with explicit configurations
			properties_content = dedent(f"""
			org.gradle.jvmargs=-Xmx3G -XX:MaxMetaspaceSize=1G
			org.gradle.daemon=false
			org.gradle.parallel=true
			org.gradle.caching=true
			
			# Java configuration
			java.toolchain.languageVersion={min_java}
			java.toolchain.vendor=ADOPTIUM
			""").strip()

			with open(os.path.join(project_dir, "gradle.properties"), "w") as f:
				f.write(properties_content)

			# Initialize/update Gradle wrapper
			gradle_cmd = (
				"gradle wrapper --gradle-version 8.10 --distribution-type=bin "
				"--warning-mode all"
			)
			run_command(gradle_cmd, cwd=project_dir, env=env)

			# Clean and build
			if os.path.isfile(os.path.join(project_dir, "gradlew")):
				run_command("./gradlew clean", cwd=project_dir, env=env)
			else:
				run_command("gradle clean", cwd=project_dir, env=env)

		except Exception as e:
			print(f"Failed to setup Gradle environment: {e}", file=sys.stderr)
			sys.exit(1)

	# Run Minecraft with more verbose output
	print(f"Running Minecraft with mod in {project_dir}...")
	try:
		if os.path.isfile(os.path.join(project_dir, "gradlew")):
			run_command(
				"./gradlew runClient --warning-mode all --stacktrace",
				cwd=project_dir,
				env=env,
			)
		else:
			run_command(
				"gradle runClient --warning-mode all --stacktrace",
				cwd=project_dir,
				env=env,
			)
	except Exception as e:
		print(f"Failed to run mod: {e}", file=sys.stderr)
		sys.exit(1)
