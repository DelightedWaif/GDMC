blocks = {
    'Cobblestone': (4,0),
    'Oak Planks': (5, 0),
    'Sandstone': (24,0),
    'Chiseled Sandstone': (24, 1),
    'Smooth Sandstone': (24, 2),
    'Oak Fence': (85, 0),
    'Stone Brick': (98, 0),
    'Acacia Fence': (192, 0)
}

# biome names come from biome_types.py
# material names are currently hardcoded
# block id's can be found at https://minecraft-ids.grahamedgecombe.com/
biomeSettings = {
	"Plains": { # Default
        "wall": blocks['Oak Planks'],
        "fence": blocks['Oak Fence'],
        "floor": blocks['Stone Brick'],
        "road": blocks['Cobblestone']
	},
	"Desert": {
        "wall": blocks['Chiseled Sandstone'], 
        "fence": blocks['Acacia Fence'],
        "floor": blocks['Sandstone'],
        "road": blocks['Smooth Sandstone']
	}
}
