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

    def __init__(self, x, z, height, type=0):
        self.x = x
        self.z = z
        self.height = height
        self.type = type
        self.biome_id = -1  # undefined by default, set in calculateBiomeMap of BlockUtils
