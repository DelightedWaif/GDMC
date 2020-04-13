from BlockTypes import blocks
# biome names come from biome_types.py
# material names are currently hardcoded
# block id's can be found at https://minecraft-ids.grahamedgecombe.com/
biomeSettings = {
    "Plains": { # Default
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Cobblestone'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Glass Pane']
    },
    "Desert": {
        "wall": blocks['Chiseled Sandstone'], 
        "fence": blocks['Acacia Fence'],
        "floor": blocks['Sandstone'],
        "road": blocks['Smooth Sandstone'],
        "door": blocks['Air'],
        'window': blocks['Glass Pane']
    },
    "Forest": {
        "wall": blocks['Dark Oak Wood Planks'],
        "fence": blocks['Dark Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Stone'],
        "door": blocks['Dark Oak Door Block'],
        'window': blocks['Glass Pane']
    },
    "Jungle": {
        "wall": blocks['Jungle Wood Planks'],
        "fence": blocks['Jungle Fence'],
        "floor": blocks['Moss Stone'],
        "road": blocks['Moss Stone'],
        "door": blocks['Jungle Door Block'],
        'window': blocks['Glass Pane']
    },
    "Taiga": {
        "wall": blocks['Spruce Wood Planks'],
        "fence": blocks['Spruce Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Chiseled Stone Bricks'],
        "door": blocks['Spruce Door Block'],
        'window': blocks['Glass Pane']   
    },
    "Swamp": {
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Moss Stone'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Glass Pane'] 
    },
    "Birch Forest": {
        "wall": blocks['Birch Wood Planks'],
        "fence": blocks['Birch Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Bricks'],
        "door": blocks['Birch Door Block'],
        'window': blocks['Glass Pane'] 
    },
    "Dark Forest": {
        "wall": blocks['Dark Oak Wood Planks'],
        "fence": blocks['Dark Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Stone'],
        "door": blocks['Dark Oak Door Block'],
        'window': blocks['Glass Pane'] 
    },
    "River Beach": {
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Stone'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Glass Pane']
    },
    "Ice": {
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Moss Stone'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Glass Pane']
    },
    "Mountains": {
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Moss Stone'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Glass Pane']
    },
    "Mushroom": {
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Polished Granite'],
        "road": blocks['Moss Stone'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Red Stained Glass Pane']
    },
	"Savanna": {
        "wall": blocks['Acacia Wood Planks'],
        "fence": blocks['Acacia Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Mossy Stone Bricks'],
        "door": blocks['Acacia Door Block'],
        'window': blocks['Glass Pane']
    },
    "Badlands": {
        "wall": blocks['White Glazed Terracotta'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Gray Glazed Terracotta'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Glass Pane']
    },
    "Aquatic": {
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Bricks'],
        "road": blocks['Mossy Stone Bricks'],
        "door": blocks['Oak Door Block'],
        'window': blocks['Glass Pane']
    }
}
