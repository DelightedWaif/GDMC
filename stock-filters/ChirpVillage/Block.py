class Block(object):

    # BLOCK TYPES
    UNASSIGNED = 0
    YARD = 1
    BUILDING = 2
    DOOR = 3
    PATH = 4

    def __init__(self, x, z, height, type=Block.UNASSIGNED):
        self.x = x
        self.z = z
        self.height = height
        self.type = type
        self.biome_id = -1  # undefined by default, set in calculateBiomeMap of BlockUtils
