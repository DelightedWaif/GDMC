import utilityFunctions
import RandUtils
from Biomes import BlockUtils


"""Utils for buildings"""

def construct_walls(level, coords, biome, height):
    minx = coords[0][0]
    minz = coords[0][1]
    miny = coords[0][2]
    maxx = coords[1][0]
    maxz = coords[1][1]
    wall_block = BlockUtils.get_wall_block(biome)
    # walls
    for y in range(height, miny, -1):
        for x in range(minx, maxx):
            for z in range(minz, maxz):
                # Skip columns since they should be a different block
                if (x == minx and z == minz) or (x == maxx-1 and z == minz) or \
                        (x == minx and z == maxz-1) or (x == maxx-1 and z == maxz-1):
                    continue
                if x == maxx-1 or z == maxz-1 or x == minx or z == minz:
                    utilityFunctions.setBlock(
                        level, wall_block, x, y, z)


def construct_floor_and_flat_roof(level, coords, biome, height):
    minx = coords[0][0]
    minz = coords[0][1]
    miny = coords[0][2]
    maxx = coords[1][0]
    maxz = coords[1][1]
    roof_block = BlockUtils.get_beam_block(biome)
    floor_block = BlockUtils.get_floor_block(biome)

    # roof and floor
    for x in range(minx, maxx):
        for z in range(minz, maxz):
            utilityFunctions.setBlock(
                level, roof_block, x, height, z)
            utilityFunctions.setBlock(
                level, floor_block, x, miny, z)

def construct_pointed_roof(level, coords, biome, height):
    minx = coords[0][0]
    minz = coords[0][1]
    miny = coords[0][2]
    maxx = coords[1][0]
    maxz = coords[1][1]
    roof_block = BlockUtils.get_beam_block(biome)
    for i in range(-1, maxx-minx/4):
        for x in range(minx+i, maxx-i):
            for z in range(minz+i, maxz-i):
                utilityFunctions.setBlock(
                    level, roof_block, x, height+i, z)

def construct_pillars(level, coords, biome, height):
    minx = coords[0][0]
    minz = coords[0][1]
    miny = coords[0][2]
    maxx = coords[1][0]
    maxz = coords[1][1]
    pillar_block = BlockUtils.get_beam_block(biome)
    for y in range(miny, height):
        for x in [minx, maxx-1]:
            for z in [minz, maxz-1]:
                utilityFunctions.setBlock(
                    level, pillar_block, x, y, z)
                
def place_door(level, coords, biome):
    minx = coords[0][0]
    minz = coords[0][1]
    miny = coords[0][2]
    maxx = coords[1][0]
    maxz = coords[1][1]
    door_block = BlockUtils.get_door_block(biome)
    # Place door
    utilityFunctions.setBlock(
        level, door_block, (minx+maxx)/2, miny+1, minz)
    utilityFunctions.setBlock(
        level, door_block, (minx+maxx)/2, miny+2, minz)

def place_windows(level, coords, biome, height_offset):
    minx = coords[0][0]
    minz = coords[0][1]
    miny = coords[0][2] + 1
    maxx = coords[1][0]
    maxz = coords[1][1]
    for i in range(0, 4):
        if i == 0:
            window_coords = ((maxx+minx)/2, miny+(2*height_offset)/3, minz)
        elif i == 1:
            window_coords = (minx, miny+(2*height_offset)/3, (maxz+minz)/2)
        elif i == 2:
            window_coords = ((maxx+minx)/2, miny +
                                (2*height_offset)/3, maxz-1)
        else:
            window_coords = (
                maxx-1, miny+(2*height_offset)/3, (maxz+minz)/2)
        if RandUtils.rand_range(maxx, minx, 100, 0) < 30:
            construct_square_window(level, window_coords, biome, i % 2)
        elif RandUtils.rand_range(maxx, minx, 100, 0) < 60:
            construct_circle_window(level, window_coords, biome, i % 2)
        else:
            construct_triangle_window(level, window_coords, biome, i % 2)

"""
    coords must be top left block
    generates window like:
    ##
    ##
"""
def construct_square_window(level, coords, biome, face=0):
    x = coords[0]
    y = coords[1]
    z = coords[2]
    window_block = BlockUtils.get_window_block(biome)
    if face == 0:
        for i in range(x, x+2):
            for j in range(y, y-2, -1):
                utilityFunctions.setBlock(
                    level, window_block, i, j, z)
    elif face == 1:
        for i in range(z, z+2):
            for j in range(y, y-2, -1):
                utilityFunctions.setBlock(
                    level, window_block, x, j, i)


"""
    coords must be top block
    generates window like:
    #
    ###
    #
"""
def construct_circle_window(level, coords, biome, face=0):
    x = coords[0]
    y = coords[1]
    z = coords[2]
    window_block = BlockUtils.get_window_block(biome)
    if face == 0:
        for j in range(y, y-3, -1):
            utilityFunctions.setBlock(
                level, window_block, x, j, z)
            if j == y-1:
                utilityFunctions.setBlock(
                    level, window_block, x-1, j, z)
                utilityFunctions.setBlock(
                    level, window_block, x+1, j, z)
    elif face == 1:
        for j in range(y, y-3, -1):
            utilityFunctions.setBlock(
                level, window_block, x, j, z)
            if j == y-1:
                utilityFunctions.setBlock(
                    level, window_block, x, j, z-1)
                utilityFunctions.setBlock(
                    level, window_block, x, j, z+1)


"""
    coords must be top block
    generates window like:
    #
    ###
"""
def construct_triangle_window(level, coords, biome, face=0):
    x = coords[0]
    y = coords[1]
    z = coords[2]
    window_block = BlockUtils.get_window_block(biome)
    if face == 0:
        for j in range(y, y-2, -1):
            utilityFunctions.setBlock(
                level, window_block, x, j, z)
            if j == y-1:
                utilityFunctions.setBlock(
                    level, window_block, x-1, j, z)
                utilityFunctions.setBlock(
                    level, window_block, x+1, j, z)
    elif face == 1:
        for j in range(y, y-2, -1):
            utilityFunctions.setBlock(
                level, window_block, x, j, z)
            if j == y-1:
                utilityFunctions.setBlock(
                    level, window_block, x, j, z-1)
                utilityFunctions.setBlock(
                    level, window_block, x, j, z+1)


def remove_blocks_in_box(level, coords):
    minx = coords[0][0]
    minz = coords[0][1]
    miny = coords[0][2]
    maxx = coords[1][0]
    maxz = coords[1][1]
    maxy = coords[1][2]
    # Sets every block in box to air
    for y in range(miny, maxy):
        for x in range(minx, maxx):
            for z in range(minz, maxz):
                utilityFunctions.setBlock(level, (0, 0), x, y, z)


"""Building Classes"""
class BasicBuilding:

    def construct(self, level, coords, surface):
        # This is assumes box is already the size of the house
        # minx = surface.to_real_x(coords[0][0])
        # minz = surface.to_real_z(coords[0][1])
        # maxx = surface.to_real_x(coords[1][0])
        # maxz = surface.to_real_z(coords[1][1])
        minx = coords[0][0]
        minz = coords[0][1]
        maxx = coords[1][0]
        maxz = coords[1][1]
        # block = surface.surface_map[minx][minz]
        miny = 63  # block.height
        biome = 1  # block.biome_id
        wall_block = BlockUtils.get_wall_block(biome)
        door_block = BlockUtils.get_door_block(biome)
        pillar_block = BlockUtils.get_beam_block(biome)
        height_offset = RandUtils.rand_range(minx, miny, 10, 5)
        pillar_height = miny + height_offset
        level_coords = ((minx, minz, miny),(maxx, maxz, pillar_height))
        remove_blocks_in_box(level, level_coords)
        construct_pillars(level, level_coords, biome, pillar_height)
        construct_walls(level, level_coords, biome, pillar_height)
        construct_floor_and_flat_roof(level, level_coords, biome, pillar_height)
        place_door(level, level_coords, biome)
        place_windows(level, level_coords, biome, height_offset)
        construct_pointed_roof(level, level_coords, biome, pillar_height)

class MultiStoryBuilding():
    def construct(self, level, coords, surface, num_stories=1):
        # This is assumes box is already the size of the house
        # minx = surface.to_real_x(coords[0][0])
        # minz = surface.to_real_z(coords[0][1])
        # maxx = surface.to_real_x(coords[1][0])
        # maxz = surface.to_real_z(coords[1][1])
        minx = coords[0][0]
        minz = coords[0][1]
        maxx = coords[1][0]
        maxz = coords[1][1]
        # block = surface.surface_map[minx][minz]
        miny = 63  # block.height
        biome = 1  # block.biome_id
        height_offset = RandUtils.rand_range(minx, miny, 10, 5)
        pillar_height = miny + height_offset
        level_coords = ((minx, minz, miny),(maxx, maxz, pillar_height))
        remove_blocks_in_box(level, level_coords)
        for i in range(0, num_stories):
            construct_pillars(level, level_coords, biome, pillar_height)
            construct_walls(level, level_coords, biome, pillar_height)
            construct_floor_and_flat_roof(level, level_coords, biome, pillar_height)
            place_windows(level, level_coords, biome, height_offset)
            if i == 0:
                place_door(level, level_coords, biome)
            level_coords = ((minx, minz, pillar_height), (maxx, maxz))
            pillar_height += height_offset


class DecoratedBuilding():
    def construct(self, level, coords, surface):
        minx = coords[0][0]
        minz = coords[0][1]
        maxx = coords[1][0]
        maxz = coords[1][1]
        # block = surface.surface_map[minx][minz]
        miny = 63  # block.height
        biome = 1  # block.biome_id
        hedge_block =  BlockUtils.get_hedge_block(biome)
        new_coords = ((minx+1, minz+1), (maxx-1, maxz-1))
        building = BasicBuilding()
        building.construct(level, new_coords, surface)
        # ring basic building in hedge
        for x in range(minx, maxx):
            for z in range(minz, maxz):
                if x == maxx-1 or z == maxz-1 or x == minx or z == minz:
                    if x != (maxx+minx)/2:
                        utilityFunctions.setBlock(level, hedge_block, x, miny, z)
                    else:
                        utilityFunctions.setBlock(level, (53, 0), x, miny, z)
