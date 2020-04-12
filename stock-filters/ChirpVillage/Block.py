class Block(object):

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.biome_id = -1; #undefined by default, set in calculateBiomeMap of BlockUtils

    def get_x(self):
        return self.x
