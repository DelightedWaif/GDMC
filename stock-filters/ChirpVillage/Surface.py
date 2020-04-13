# coding=utf-8
"""
    Surface.py
    Surface Class
        Used for 2d representation of level
    Author: Chirp Nets
    © 2020
"""

from Block import Block


class Surface(object):

    def __init__(self, level, box):
        self.x_start = box.minx
        self.z_start = box.minz
        self.x_end = box.maxx
        self.z_end = box.maxz
        self.x_length = self.x_end - self.x_start
        self.z_length = self.z_end - self.z_start
        self.surface_map = self.init_surface_map(level)
        self.door_blocks = [(0,0), (3,0), (7,4), (15, 4)]
        self.test_buildings = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]

    def set_surface_map(self, surface_map):
        self.surface_map = surface_map

    def init_surface_map(self, level):
        """
        Initialize the surface_map with data from the world's level
        :param level: level object which stores the worlds blocks and block data
        :return: initialized surface_map filled with correct data from level
        """
        surface_map = []
        for i in range(self.x_length):
            row = []
            for j in range(self.z_length):
                row.append(Block(i, j, self.get_height(i, j, level), Block.UNASSIGNED))
            surface_map.append(row)
        return surface_map

    def populate_surface_map(self):
        for point in self.test_buildings:
            x = point[0]
            z = point[1]
            block = self.surface_map[x][z]
            block.set_type(1)
        for point in self.door_blocks:
            x = point[0]
            z = point[1]
            block = self.surface_map[x][z]
            block.set_type(3)
        print(self.surface_map)

    @staticmethod
    def get_height(x, z, level):
        """
        Find the first ground block before air using a binary search.
        :param x: x-coord to the block
        :param z: z-coord to the block
        :param level: level object which stores the worlds blocks and block data
        :return: height (y-value) of the first ground block before air.
        """
        top = 255
        bottom = 0
        y = 128  # Start at halfway.
        found = False
        while not found:
            block = level.blockAt(x, y, z)
            if block == 0:
                neighbour_below = level.blockAt(x, y-1, z)
                if neighbour_below != 0:
                    return y-1
                else:
                    top = y
                    y = y - int(round(float(y - bottom)/2))
            else:
                neighbour_above = level.blockAt(x, y + 1, z)
                if neighbour_above == 0:
                    return y+1
                else:
                    bottom = y
                    y = y + int(round(float(top - y)/2))

    def to_real_x(self, x):
        """
        Convert the surface x value to a real world x value
        :return: offset x value which is the real world x value
        """
        return self.x_start + x

    def to_real_z(self, z):
        """
        Convert the surface z value to a real world z value
        :return: offset z value which is the real world z value
        """
        return self.z_start + z

    def visualize(self):
        """
        Visualize the surface.surface_map by printing out
        predefined symbols for Block.types
        :return: void
        """
        print("Surface Looks Like: \n")
        print("| " + "".join([" + " for _ in range(self.x_length)]) + " |")
        for j in range(self.z_length):
            row = ["|"]
            for i in range(self.x_length):
                row.append("_" if self.surface_map[i][j].type == Block.YARD else
                           "#" if self.surface_map[i][j].type == Block.BUILDING else
                           "X" if self.surface_map[i][j].type == Block.DOOR else
                           "@" if self.surface_map[i][j].type == Block.PATH else
                           " ")
            row.append("|")
            print("  ".join(row))
        print("| " + "".join([" + " for _ in range(self.x_length)]) + " |")