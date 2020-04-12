from BiomeSettings import biomeSettings
from pymclevel.biome_types import biome_types

# gets the name of the biome, if the biome is not supported, returns 'Plains' biome
def get_biome_name(biome):
    biomeName = biome_types[biome]
    if biomeName in biomeSettings:
        return biomeName
    else:
        return 'Plains'

# getters for various biome specific blocks
def get_wall_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['wall'];

def get_floor_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['floor'];

def get_fence_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['fence'];

def get_road_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['road'];

# adds biome id's to all blocks in a provided surface object
def calculateBiomeMap(level, surface):
	for x in range(surface.x_start, surface.x_end):
		for z in range(surface.z_start, surface.z_end):
			chunk = level.getChunk(x / 16, z / 16)
			chunkBiomeData = chunk.root_tag["Level"]["Biomes"].value
			surface.surface_map[x - surface.x_start][z -
			    surface.z_start].biome_id = chunkBiomeData[chunkIndexToBiomeDataIndexV2(x % 16, z % 16)]

def chunkIndexToBiomeDataIndexV2(x, z):
	return 255 - ((15 - x) + (15 - z) * 16)
