"""generator.py

Responsible for generating the Java code and a Gradle build script for a Fabric mod.
"""

import os
from textwrap import dedent


def generate_mod_project(mod_config, blocks, items, output_dir):
	"""Generates the entire mod project (Java code, resources, build files)
	in the specified output directory.

	:param mod_config: ModConfig instance with mod metadata
	:param blocks: List of Block instances
	:param items: List of Item instances
	:param output_dir: Where to place the generated mod project
	"""
	# 1. Create directory structure
	src_main_java = os.path.join(output_dir, "src", "main", "java", mod_config.mod_id)
	src_main_resources = os.path.join(output_dir, "src", "main", "resources")
	os.makedirs(src_main_java, exist_ok=True)
	os.makedirs(src_main_resources, exist_ok=True)

	# 2. Generate a basic build.gradle (very simplified for demonstration)
	build_gradle_content = dedent(f"""
    plugins {{
        id 'java'
        id 'fabric-loom' version '1.0-SNAPSHOT' // Example placeholder
    }}

    repositories {{
        mavenCentral()
        maven {{"url" "https://maven.fabricmc.net/"}}
    }}

    dependencies {{
        minecraft "com.mojang:minecraft:{mod_config.mc_version}"
        mappings "net.fabricmc:yarn:{mod_config.mc_version}+build.1" // Example placeholder
        modImplementation "net.fabricmc:fabric-loader:0.14.0" // Example placeholder
    }}

    group = "com.example"
    version = "{mod_config.version}"
    archivesBaseName = "{mod_config.mod_id}"
    """).strip()

	with open(os.path.join(output_dir, "build.gradle"), "w", encoding="utf-8") as f:
		f.write(build_gradle_content)

	# 3. Create a minimal fabric.mod.json (used by Fabric to define the mod)
	fabric_mod_json_content = {
		"schemaVersion": 1,
		"id": mod_config.mod_id,
		"version": mod_config.version,
		"name": mod_config.mod_name,
		"description": mod_config.description,
		"entrypoints": {
			"main": [f"{mod_config.mod_id}.{mod_config.mod_id.capitalize()}"],
		},
		"depends": {"fabricloader": "*", "minecraft": mod_config.mc_version},
	}

	import json

	with open(
		os.path.join(src_main_resources, "fabric.mod.json"),
		"w",
		encoding="utf-8",
	) as f:
		json.dump(fabric_mod_json_content, f, indent=4)

	# 4. Generate a main mod class (Java) with basic registration calls
	java_main_class = dedent(f"""
    package {mod_config.mod_id};

    import net.fabricmc.api.ModInitializer;

    public class {mod_config.mod_id.capitalize()} implements ModInitializer {{
        @Override
        public void onInitialize() {{
            System.out.println("Loading {mod_config.mod_name}...");
            // Register blocks
            registerBlocks();
            // Register items
            registerItems();
        }}

        private void registerBlocks() {{
            // For demonstration, you'll probably use Registry.register(...)
    """)
	for block in blocks:
		java_main_class += f'            System.out.println("Registering block: {block.name} ({block.block_id})");\n'
	java_main_class += "        }\n\n"
	java_main_class += dedent("""
        private void registerItems() {
    """)
	for item in items:
		java_main_class += f'            System.out.println("Registering item: {item.name} ({item.item_id})");\n'
	java_main_class += dedent("""
        }
    }
    """)

	with open(
		os.path.join(src_main_java, f"{mod_config.mod_id.capitalize()}.java"),
		"w",
		encoding="utf-8",
	) as f:
		f.write(java_main_class)

	# 5. (Optional) Copy or generate placeholder textures
	#    If you have real PNG files, you'd place them in resources/assets/<mod_id>/textures/...
	assets_textures_blocks = os.path.join(
		src_main_resources,
		"assets",
		mod_config.mod_id,
		"textures",
		"block",
	)
	assets_textures_items = os.path.join(
		src_main_resources,
		"assets",
		mod_config.mod_id,
		"textures",
		"item",
	)
	os.makedirs(assets_textures_blocks, exist_ok=True)
	os.makedirs(assets_textures_items, exist_ok=True)

	for block in blocks:
		# Just create a placeholder file for demonstration
		with open(
			os.path.join(assets_textures_blocks, block.texture_file),
			"wb",
		) as img:
			img.write(b"\x89PNG\r\n\x1a\n")  # minimal PNG header

	for item in items:
		with open(os.path.join(assets_textures_items, item.texture_file), "wb") as img:
			img.write(b"\x89PNG\r\n\x1a\n")  # minimal PNG header

	print(f"Mod project generated in: {output_dir}")
