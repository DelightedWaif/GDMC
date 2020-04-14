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
        self.door_blocks = []

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
        real x = surface x + start of surface
        :return: offset x value which is the real world x value
        """
        return self.x_start + x

    def to_real_z(self, z):
        """
        Convert the surface z value to a real world z value
        real z = surface z + start of surface
        :return: offset z value which is the real world z value
        """
        return self.z_start + z

    def to_surface_x(self, x):
        """
        Convert the real x value to a surface x value
        surface x = real x - start of surface
        :return: offset x value which is the surface x value
        """
        return x - self.x_start

    def to_surface_z(self, z):
        """
        Convert the real z value to a surface z value
        surface z = real z - start of surface
        :return: offset z value which is the surface z value
        """
        return z - self.z_start

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
