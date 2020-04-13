import utilityFunctions
import random


class BasicBuilding:

    def construct(self, level, coords, surface):
        # This is assumes box is already the size of the house
        minx = coords[0][0]
        minz = coords[0][1]
        maxx = coords[1][0]
        maxz = coords[1][1]
        miny = 63
        wall_block = 5
        door_block = 193
        pillar_height = miny + random.randrange(5, 10)
        for y in range(miny, pillar_height):
            for x in [minx, maxx-1]:
                for z in [minz, maxz-1]:
                    utilityFunctions.setBlock(
                        level, (wall_block, 0), x, y, z)
        # walls
        for y in range(pillar_height, miny, -1):
            for x in range(minx, maxx):
                for z in range(minz, maxz):
                    # Skip columns since they should always be walls
                    if (x == minx and z == minz) or (x == maxx-1 and z == minz) or \
                            (x == minx and z == maxz-1) or (x == maxx-1 and z == maxz-1):
                        continue
                    # This follows the CA described in the documentation
                    # set to wall if it is a wall
                    if x == maxx-1 or z == maxz-1 or x == minx or z == minz:
                        utilityFunctions.setBlock(
                            level, (wall_block, 0), x, y, z)
        # roof and floor
        for x in range(minx, maxx):
            for z in range(minz, maxz):
                utilityFunctions.setBlock(
                    level, (wall_block, 0), x, pillar_height, z)
                utilityFunctions.setBlock(
                    level, (wall_block, 0), x, miny, z)
        # Place door
        utilityFunctions.setBlock(
            level, (door_block, 0), (minx+maxx)/2, miny+1, minz)
        utilityFunctions.setBlock(
            level, (door_block, 0), (minx+maxx)/2, miny+2, minz)

    # coords must include top left block
    # generates window like:
    # ##
    # ##
    def construct_square_window(self, level, coords, surface, face=0):
        x = coords[0]
        y = coords[1]
        z = coords[2]
        window_block = 102
        if face == 0:
            for i in range(x, x+1):
                for j in range(y, y-1, -1):
                    utilityFunctions.setBlock(
                        level, (window_block, 0), i, j, z)
        elif face == 1:
            for i in range(z, z+1):
                for j in range(y, y-1, -1):
                    utilityFunctions.setBlock(
                        level, (window_block, 0), x, j, i)

    # coords must include top block
    # generates window like:
    #  #
    # ###
    #  #
    def construct_circle_window(self, level, coords, surface, face=0):
        x = coords[0]
        y = coords[1]
        z = coords[2]
        window_block = 102
        if face == 0:
            for j in range(y, y-2, -1):
                utilityFunctions.setBlock(
                    level, (window_block, 0), x, j, z)
                if j == y-1:
                    utilityFunctions.setBlock(
                            level, (window_block, 0), x-1, j, z)
                    utilityFunctions.setBlock(
                        level, (window_block, 0), x+1, j, z)
        elif face == 1:
            for j in range(y, y-2, -1):
                utilityFunctions.setBlock(
                    level, (window_block, 0), x, j, z)
                if j == y-1:
                    utilityFunctions.setBlock(
                        level, (window_block, 0), x, j, z-1)
                    utilityFunctions.setBlock(
                        level, (window_block, 0), x, j, z+1)


def remove_blocks_in_box(self, level, box):
    # Sets every block in box to air
    for y in range(box.miny, box.maxy):
        for x in range(box.minx, box.maxx):
            for z in range(box.minz, box.maxz):
                utilityFunctions.setBlock(level, (0, 0), x, y, z)


class TwoStoryBuilding():
    def construct(self, level, coords, surface):
        minx = coords[0][0]
        minz = coords[0][1]
        maxx = coords[1][0]
        maxz = coords[1][1]
        miny = 70  # surface.surface_map[minx][minz].height
        wall_block = 5
        window_block = 102
        column_block = 17
        door_block = 193
        pillar_height = miny + random.randrange(5, 10)


class DecoratedBuilding():
    def construct(self, level, coords, surface):
        pass
