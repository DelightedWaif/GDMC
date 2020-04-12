from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import utilityFunctions
import BlockUtils


class BasicBuilding():
    def __init__(self, level, box, surface, block_id=98, block_type=0, height=5):
        self.biome = surface.surface_map[0][0].biome_id
        details = {'height': height, 'wall': BlockUtils.get_wall_block(self.biome)}
        self.construct_walls(level, box, details)
        self.construct_roof(level, box, details)
        self.construct_floor(level, box)

    def construct_walls(self, level, box, details):
        # build walls
        for x in range(box.minx, box.maxx):
            for z in range(box.minz, box.maxz):
                for y in range(box.miny, box.miny+details['height']):
                    if x == box.maxx-1 or z == box.maxz-1 or x == box.minx or z == box.minz:
                        if (y % 3 == 2):
                            utilityFunctions.setBlock(
                                level, (160, 3), x, y, z)
                        else:
                            utilityFunctions.setBlock(
                                level, details['wall'], x, y, z)
                    # Check if building is empty
                    elif level.blockAt(x, y, z) != 0:
                        utilityFunctions.setBlock(
                            level, (0, 0), x, y, z)
                    # add door
                    elif x == box.minx and z == round(box.maxz / 2) and y == box.miny:
                        print("doing door")
                        utilityFunctions.setBlock(
                            level, (64, 0), x, y, z)

    def construct_roof(self, level, box, details):
        # build roof
        for x in range(box.minx, box.maxx):
            for z in range(box.minz, box.maxz):
                utilityFunctions.setBlock(
                    level, details['wall'], x, box.miny + details['height'], z)

    def construct_floor(self, level, box):
        # This is where we build a floor
        for x in range(box.minx, box.maxx):
            for z in range(box.minz, box.maxz):
                utilityFunctions.setBlock(level, BlockUtils.get_floor_block(self.biome), x, box.miny, z)
