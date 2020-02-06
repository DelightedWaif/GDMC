from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import utilityFunctions

inputs = (
    ('cs4303', 'label'),
    ('Material1', alphaMaterials.StoneBricks),
    ('Creator: ChirpNets', 'label'),
)


def perform(level, box, options):
    wall_details = {'height': 5, 'block': (98, 0)}
    construct_walls(level, box, wall_details)
    construct_roof(level, box, wall_details)
    construct_floor(level, box)


def construct_building(level, box, type):
    # This is where we build a building
    pass


def construct_floor(level, box):
    # This is where we build a floor
    for x in range(box.minx, box.maxx):
        for z in range(box.minz, box.maxz):
            utilityFunctions.setBlock(level, (98, 0), x, box.miny, z)


def construct_pillars(level, box):
    # This is where we build pillars
    pass


def construct_walls(level, box, details):
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
                            level, details['block'], x, y, z)
                elif level.blockAt(x, y, z) != 0:
                    utilityFunctions.setBlock(
                        level, (0, 0), x, y, z)


def construct_roof(level, box, details):

    # build roof
    for x in range(box.minx, box.maxx):
        for z in range(box.minz, box.maxz):
            utilityFunctions.setBlock(
                level, details['block'], x, box.miny+details['height'], z)


def build_paths(level, box):
    # this is where we build paths
    pass
