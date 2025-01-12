"""generator.py

Responsible for generating the Java code and a Gradle build script for a Fabric mod.
"""

import os
import shutil
import sys  # For error handling
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

	# Create gradle wrapper directory
	gradle_wrapper_dir = os.path.join(output_dir, "gradle", "wrapper")
	os.makedirs(gradle_wrapper_dir, exist_ok=True)

	# Generate gradle-wrapper.properties
	wrapper_properties = dedent("""
    distributionBase=GRADLE_USER_HOME
    distributionPath=wrapper/dists
    distributionUrl=https\\://services.gradle.org/distributions/gradle-8.10-bin.zip
    networkTimeout=10000
    zipStoreBase=GRADLE_USER_HOME
    zipStorePath=wrapper/dists
    """).strip()

	with open(
		os.path.join(gradle_wrapper_dir, "gradle-wrapper.properties"),
		"w",
		encoding="utf-8",
	) as f:
		f.write(wrapper_properties)

	# Generate settings.gradle
	settings_gradle_content = dedent(f"""
    pluginManagement {{
        repositories {{
            maven {{
                url = uri('https://maven.fabricmc.net/')
                name = 'Fabric'
            }}
            gradlePluginPortal()
            mavenCentral()
        }}
    }}
    rootProject.name = '{mod_config.mod_id}'
    """).strip()

	# 2. Generate a basic build.gradle
	min_java, rec_java = mod_config.get_required_java_version()
	loom_version = mod_config.get_fabric_loom_version()

	build_gradle_content = dedent(f"""
    plugins {{
        id 'fabric-loom' version '{loom_version}'
        id 'java'
        id 'java-library'
    }}

    group = '{mod_config.group}'
    version = '{mod_config.version}'

    repositories {{
        mavenCentral()
        maven {{
            url = uri("https://maven.fabricmc.net/")
        }}
        maven {{
            url = uri("https://api.modrinth.com/maven")  // Additional repository
        }}
    }}

    dependencies {{
        minecraft "com.mojang:minecraft:{mod_config.mc_version}"
        mappings "net.fabricmc:yarn:{mod_config.mc_version}+build.1:v2"
        modImplementation "net.fabricmc:fabric-loader:0.16.9"  // Ensure this matches your Fabric Loader version
        modImplementation "net.fabricmc.fabric-api:fabric-api:{mod_config.get_fabric_api_version()}"
    }}

    java {{
        toolchain {{
            languageVersion = JavaLanguageVersion.of({min_java})
        }}
        sourceCompatibility = JavaVersion.VERSION_{min_java}
        targetCompatibility = JavaVersion.VERSION_{min_java}
    }}

    tasks.withType(JavaCompile).configureEach {{
        it.options.encoding = "UTF-8"
        it.options.release = {min_java}
    }}

    tasks.withType(Test).configureEach {{
        useJUnitPlatform()
        javaLauncher = javaToolchains.launcherFor {{
            languageVersion = JavaLanguageVersion.of({min_java})
        }}
    }}

    tasks.withType(JavaExec).configureEach {{
        javaLauncher = javaToolchains.launcherFor {{
            languageVersion = JavaLanguageVersion.of({min_java})
        }}
    }}
    """).strip()

	# Write settings.gradle
	with open(os.path.join(output_dir, "settings.gradle"), "w", encoding="utf-8") as f:
		f.write(settings_gradle_content)

	# Write build.gradle
	with open(os.path.join(output_dir, "build.gradle"), "w", encoding="utf-8") as f:
		f.write(build_gradle_content)

	# 3. Create fabric.mod.json instead of mods.toml
	meta_inf_dir = os.path.join(src_main_resources, "META-INF")
	os.makedirs(meta_inf_dir, exist_ok=True)

	fabric_mod_json = {
		"schemaVersion": 1,
		"id": mod_config.mod_id,
		"version": mod_config.version,
		"name": mod_config.mod_name,
		"description": mod_config.description,
		"authors": mod_config.authors,
		"contact": mod_config.contact,
		"license": "MIT",
		"environment": "*",
		"entrypoints": {
			"main": [f"{mod_config.mod_id}.{mod_config.mod_id.capitalize()}"]
		},
		"depends": {
			"fabricloader": ">=0.14.24",
			"minecraft": f">={mod_config.mc_version}",
			"java": f">={min_java}",
		},
	}

	with open(
		os.path.join(src_main_resources, "fabric.mod.json"),
		"w",
		encoding="utf-8",
	) as f:
		import json

		json.dump(fabric_mod_json, f, indent=2)

	# 4. Create localization file: lang/en_us.json
	lang_dir = os.path.join(src_main_resources, "assets", mod_config.mod_id, "lang")
	os.makedirs(lang_dir, exist_ok=True)

	en_us_json_content = {f"item.{mod_config.mod_id}.example_item": "Example Item"}

	with open(
		os.path.join(lang_dir, "en_us.json"),
		"w",
		encoding="utf-8",
	) as f:
		import json

		json.dump(en_us_json_content, f, indent=4)

	# 5. Create item model JSON with correct texture path
	models_item_dir = os.path.join(
		src_main_resources, "assets", mod_config.mod_id, "models", "item"
	)
	os.makedirs(models_item_dir, exist_ok=True)

	# Create the model JSON with a texture path matching the actual filename
	example_item_json_content = {
		"parent": "item/generated",
		"textures": {
			# Strip .png extension if present and use the basename
			"layer0": f"{mod_config.mod_id}:item/{os.path.splitext(os.path.basename(items[0].texture_file))[0]}"
		},
	}

	with open(
		os.path.join(models_item_dir, "example_item.json"),
		"w",
		encoding="utf-8",
	) as f:
		json.dump(example_item_json_content, f, indent=4)

	# 6. Generate a main mod class with proper Item initialization
	java_main_class = dedent(f"""
    package {mod_config.mod_id};

    import net.fabricmc.api.ModInitializer;
    import net.minecraft.item.Item;
    import net.minecraft.item.ItemGroups;
    import net.minecraft.registry.Registries;
    import net.minecraft.registry.Registry;
    import net.minecraft.util.Identifier;
    import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;

    public class {mod_config.mod_id.capitalize()} implements ModInitializer {{
        public static final String MOD_ID = "{mod_config.mod_id}";
        
        private static Identifier makeId(String path) {{
            System.out.println("[" + MOD_ID + "] Creating Identifier: " + MOD_ID + ":" + path);
            return new Identifier(MOD_ID, path);  // Use constructor directly
        }}

        // Register item with proper translation key and settings
        public static final Item EXAMPLE_ITEM = Registry.register(
            Registries.ITEM,
            makeId("example_item"),
            new Item(new Item.Settings().translationKey(MOD_ID + ".example_item"))
        );

        @Override
        public void onInitialize() {{
            System.out.println("[" + MOD_ID + "] Initializing mod...");
            System.out.println("[" + MOD_ID + "] Item registered as: " + EXAMPLE_ITEM.getTranslationKey());
            System.out.println("[" + MOD_ID + "] Item identifier: " + Registry.ITEM.getId(EXAMPLE_ITEM));
            
            ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> {{
                entries.add(EXAMPLE_ITEM);
                System.out.println("[" + MOD_ID + "] Added " + EXAMPLE_ITEM.toString() + " to ingredients group");
            }});
            
            System.out.println("[" + MOD_ID + "] Initialization complete for {mod_config.mod_name}");
        }}
    }}
    """).strip()

	with open(
		os.path.join(src_main_java, f"{mod_config.mod_id.capitalize()}.java"),
		"w",
		encoding="utf-8",
	) as f:
		f.write(java_main_class)

	# 7. Copy textures with correct naming
	assets_textures_item_dir = os.path.join(
		src_main_resources,
		"assets",
		mod_config.mod_id,
		"textures",
		"item",
	)
	os.makedirs(assets_textures_item_dir, exist_ok=True)

	for item in items:
		source_texture = os.path.abspath(item.texture_file)
		# Use example_item.png as the destination name to match the model reference
		destination_texture = os.path.join(assets_textures_item_dir, "example_item.png")
		if os.path.exists(source_texture):
			try:
				shutil.copyfile(source_texture, destination_texture)
				print(f"Copied item texture: {item.texture_file} -> example_item.png")
			except Exception as e:
				print(f"Error copying item texture: {e}", file=sys.stderr)
				sys.exit(1)
		else:
			print(f"Error: Texture file not found: {source_texture}", file=sys.stderr)
			sys.exit(1)

	# Handle block textures similarly if blocks are provided
	if blocks:
		assets_textures_block_dir = os.path.join(
			src_main_resources,
			"assets",
			mod_config.mod_id,
			"textures",
			"block",
		)
		os.makedirs(assets_textures_block_dir, exist_ok=True)

		for block in blocks:
			source_texture = os.path.abspath(block.texture_file)
			destination_texture = os.path.join(
				assets_textures_block_dir, os.path.basename(block.texture_file)
			)
			if os.path.exists(source_texture):
				try:
					shutil.copyfile(source_texture, destination_texture)
					print(f"Copied block texture: {block.texture_file}")
				except Exception as e:
					print(
						f"Error copying block texture '{block.texture_file}': {e}",
						file=sys.stderr,
					)
					sys.exit(1)
			else:
				print(
					f"Error: Block texture file '{source_texture}' does not exist.",
					file=sys.stderr,
				)
				sys.exit(1)

	print(f"Mod project generated in: {output_dir}")
