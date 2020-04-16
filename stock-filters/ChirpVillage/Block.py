# coding=utf-8
"""
    Block.py
        Block class used to represent blocks within a surface's surface_map
    Author: Chirp Nets
    © 2020
"""


class Block(object):

    # BLOCK TYPES
    UNASSIGNED = 0
    YARD = 1
    BUILDING = 2
    DOOR = 3
    PATH = 4
    BUILDING_DOOR = 5

    def __init__(self, x, z, height, type=UNASSIGNED):
        self.x = x
        self.z = z
        self.height = height
        self.steepness = -1  # undefined by default, set in surface constructor
        self.type = type
        self.biome_id = -1  # undefined by default, set in calculateBiomeMap of BlockUtils
        self.is_water = False
        self.is_lava = False
        self.path_placed = False
