blocks = {
    'Air': (0, 0),
    'Stone': (1, 0),
    'Grass': (2,0),
    'Dirt': (3, 0),
    'Cobblestone': (4,0),
    'Oak Wood Planks': (5, 0),
    'Spruce Wood Planks': (5, 1),
    'Birch Wood Planks': (5, 2),
    'Jungle Wood Planks': (5, 3),
    'Acacia Wood Planks': (5, 4),
    'Dark Oak Wood Planks': (5, 5),
    'Still Water': (9, 0),
    'Sand': (12, 0),
    'Gravel': (13, 0),
    'Oak Wood': (17,0),
    'Spruce Wood': (17, 1),
    'Birch Wood': (17, 2),
    'Jungle Wood': (17, 3),
    'Sandstone': (24,0),
    'Chiseled Sandstone': (24, 1),
    'Smooth Sandstone': (24, 2),
    'Moss Stone': (48, 0),
    'Oak Door Block': (64,0),
    'Oak Fence': (85, 0),
    'Stone Brick': (98, 0),
    'Glass Pane': (102, 0),
    'Spruce Fence': (188, 0),
    'Birch Fence': (189, 0),
    'Jungle Fence': (190, 0),
    'Dark Oak Fence': (191, 0),		
    'Acacia Fence': (191, 0),
    'Spruce Door Block': (193, 0),
    'Birch Door Block': (194, 0),
    'Jungle Door Block': (195, 0),
    'Acacia Door Block': (196, 0),
    'Dark Oak Door Block': (197, 0)
}

# biome names come from biome_types.py
# material names are currently hardcoded
# block id's can be found at https://minecraft-ids.grahamedgecombe.com/
biomeSettings = {
	"Plains": { # Default
        "wall": blocks['Oak Wood Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Brick'],
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
        "floor": blocks['Stone Brick'],
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
    }
}
