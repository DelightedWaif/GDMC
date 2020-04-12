class Block(object):

    # BLOCK TYPES
    UNASSIGNED = 0
    YARD = 1
    BUILDING = 2
    DOOR = 3
    PATH = 4

    def __init__(self, x, z, height):
        self.x = x
        self.y = z
        self.height = height
        self.type = 0
        self.biome_id = -1 #undefined by default, set in calculateBiomeMap of BlockUtils
