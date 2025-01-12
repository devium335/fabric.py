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

	# Create gradle wrapper directory
	gradle_wrapper_dir = os.path.join(output_dir, "gradle", "wrapper")
	os.makedirs(gradle_wrapper_dir, exist_ok=True)

	# Generate gradle-wrapper.properties
	wrapper_properties = dedent("""
    distributionBase=GRADLE_USER_HOME
    distributionPath=wrapper/dists
    distributionUrl=https\\://services.gradle.org/distributions/gradle-8.1.1-bin.zip
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

	build_gradle_content = dedent(f"""
    plugins {{
        id 'fabric-loom' version '1.4.+'
        id 'java'
        id 'java-library'
    }}

    base.archivesName = project.name
    version = "{mod_config.version}"
    group = "com.example"

    repositories {{
        maven {{ url = uri("https://maven.fabricmc.net/") }}
        mavenCentral()
        maven {{ url = uri("https://api.modrinth.com/maven") }}  // Additional repository
        maven {{ url = uri("https://maven.quiltmc.org/repository/release") }}  // For some Fabric dependencies
    }}

    dependencies {{
        minecraft "com.mojang:minecraft:{mod_config.mc_version}"
        mappings "net.fabricmc:yarn:{mod_config.mc_version}+build.1:v2"
        modImplementation "net.fabricmc:fabric-loader:0.15.3"  // Updated loader version
        modImplementation "net.fabricmc.fabric-api:fabric-api:{mod_config.get_fabric_api_version()}"
    }}

    java {{
        toolchain {{
            languageVersion = JavaLanguageVersion.of({min_java})
            vendor = JvmVendorSpec.ADOPTIUM
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

	# Create gradle.properties
	gradle_properties = dedent(f"""
    org.gradle.jvmargs=-Xmx3G -XX:MaxMetaspaceSize=1G
    org.gradle.daemon=false
    org.gradle.parallel=true
    org.gradle.caching=true
    
    // Java configuration
    java.toolchain.languageVersion={min_java}
    java.toolchain.vendor=ADOPTIUM
    """).strip()

	with open(
		os.path.join(output_dir, "gradle.properties"), "w", encoding="utf-8"
	) as f:
		f.write(gradle_properties)

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
	print(f"Mod project generated in: {output_dir}")
