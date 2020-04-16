from BiomeSettings import biomeSettings
from BiomeMapping import biome_map

# gets the name of the biome, if the biome is not supported, returns 'Plains' biome
def get_biome_name(biome):
    for key, value in biome_map.items():
        if biome in value:
            return key
    return 'Plains'

# getters for various biome specific blocks
def get_wall_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['wall']

def get_floor_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['floor']

def get_fence_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['fence']

def get_road_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['road']

def get_door_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['door']
    
def get_window_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['window']

def get_beam_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['beam']

def get_hedge_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['hedge']

def get_roof_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['roof']

def get_crop_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['crop']

def get_soil_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['soil']

def get_bridge_block(biome=1):
    biomeName = get_biome_name(biome)
    return biomeSettings[biomeName]['bridge']

# adds biome id's to all blocks in a provided surface object
# works by collecting chunk index from each level chunk, converting to biome id
# and adding that to surface
def calculate_biomes_on_surface(level, surface):
    for x in range(surface.x_start, surface.x_end):
        for z in range(surface.z_start, surface.z_end):
            chunk = level.getChunk(x / 16, z / 16)
            chunkBiomeData = chunk.root_tag["Level"]["Biomes"].value
            surface.surface_map[x - surface.x_start][z -
                surface.z_start].biome_id = chunkBiomeData[chunk_index_to_biome_id(x % 16, z % 16)]

# coverts id returned by chunk to biome id
def chunk_index_to_biome_id(x, z):
    return 255 - ((15 - x) + (15 - z) * 16)
