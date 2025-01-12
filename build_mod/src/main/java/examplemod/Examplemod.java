
package examplemod;

import net.fabricmc.api.ModInitializer;

public class Examplemod implements ModInitializer {
    @Override
    public void onInitialize() {
        System.out.println("Loading Example Mod...");
        // Register blocks
        registerBlocks();
        // Register items
        registerItems();
    }

    private void registerBlocks() {
        // For demonstration, you'll probably use Registry.register(...)
        }


private void registerItems() {
            System.out.println("Registering item: My Item (my_item)");

    }
}
