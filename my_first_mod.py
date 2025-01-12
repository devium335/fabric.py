from fabricpy import Item, ModConfig

mod_config = ModConfig(
	mod_name="Example Mod",
	mod_id="examplemod",
	mc_version="1.21.4",
	group="com.example",  # Optional: defaults to mod_id if not specified
)

items = [Item("my_item", "My Item", texture_file="example.png", category="misc")]
