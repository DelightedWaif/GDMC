import utilityFunctions
import random


class Building(object):

    def construct(self, level, box):
        # This is assumes box is already the size of the house
        pillar_height = box.miny + random.randrange(5, 10)
        for y in range(box.miny, pillar_height):
            for x in [box.minx, box.maxx-1]:
                for z in [box.minz, box.maxz-1]:
                    utilityFunctions.setBlock(level, (1, 0), x, y, z)
        # walls
        for i in range(0, 200):
            for x in range(box.minx, box.maxx):
                for z in range(box.minz, box.maxz):
                    # Skip columns since they should always be walls
                    if (x == box.minx and z == box.minz) or (x == box.maxx-1 and z == box.minz) or (x == box.minx and z == box.maxz-1) or (x == box.maxx-1 and z == box.maxz-1):
                        continue
                    for y in range(box.miny, pillar_height):
                        if x == box.maxx-1 or z == box.maxz-1 or x == box.minx or z == box.minz:
                            if level.blockAt(x, y, z) == 0:
                                utilityFunctions.setBlock(
                                    level, (1, 0), x, y, z)
                            elif level.blockAt(x, y - 1, z) == 1 and level.blockAt(x, y + 1, z) == 1:
                                if random.uniform(0, 1) < 0.8:
                                    utilityFunctions.setBlock(
                                        level, (1, 0), x, y, z)
                                else:
                                    utilityFunctions.setBlock(
                                        level, (102, 0), x, y, z)
                            elif level.blockAt(x, y - 1, z) == 102 and level.blockAt(x, y + 1, z) == 102:
                                if random.uniform(0, 1) < 0.9:
                                    utilityFunctions.setBlock(
                                        level, (1, 0), x, y, z)
                                else:
                                    utilityFunctions.setBlock(
                                        level, (102, 0), x, y, z)
                            elif level.blockAt(x, y-1, z) == 1 and level.blockAt(x, y+1, z) != 1 or level.blockAt(x, y-1, z) != 1 and level.blockAt(x, y+1, z) == 1:
                                if random.uniform(0, 1) < 0.5:
                                    utilityFunctions.setBlock(
                                        level, (1, 0), x, y, z)
                                else:
                                    utilityFunctions.setBlock(
                                        level, (102, 0), x, y, z)
        # roof and floor
        for x in range(box.minx, box.maxx):
            for z in range(box.minz, box.maxz):
                utilityFunctions.setBlock(
                    level, (1, 0), x, pillar_height, z)
                utilityFunctions.setBlock(
                    level, (1, 0), x, box.miny, z)

    def remove_blocks_in_box(self, level, box):
        # Sets every block in box to air
        for y in range(box.miny, box.maxy):
            for x in range(box.minx, box.maxx):
                for z in range(box.minz, box.maxz):
                    utilityFunctions.setBlock(level, (0, 0), x, y, z)
