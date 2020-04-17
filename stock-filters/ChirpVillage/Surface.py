# coding=utf-8
"""
    Surface.py
    Surface Class
        Used for 2d representation of level
    Author: Chirp Nets
    © 2020
"""

from Block import Block
from Biomes.BlockTypes import surface_blocks, blocks
from copy import copy


class Surface(object):

    def __init__(self, level, box):
        self.x_start = box.minx
        self.y_start = box.miny
        self.z_start = box.minz
        self.x_end = box.maxx
        self.y_end = box.maxy
        self.z_end = box.maxz
        self.x_length = abs(self.x_end - self.x_start)
        self.z_length = abs(self.z_end - self.z_start)
        self.surface_map = self.init_surface_map(level)
        self.surface_map = self.calc_steepness()
        self.surface_map = self.find_waterways(level)
        self.calculate_biomes_on_surface(level)
        self.door_blocks = []

    def calculate_biomes_on_surface(self, level):
        """
        adds biome id's to all blocks in a provided surface object
        works by collecting chunk index from each level chunk, converting to biome id
        and adding that to surface
        """
        for x in range(self.x_start, self.x_end):
            for z in range(self.z_start, self.z_end):
                chunk = level.getChunk(x / 16, z / 16)
                chunk_biomes = chunk.root_tag["Level"]["Biomes"].value
                self.surface_map[x - self.x_start][z -
                    self.z_start].biome_id = chunk_biomes[(x % 16) * 16 + (z % 16)]

    def find_waterways(self, level):
        """
        find water systems in the surface_map.
        :return: new_surface_map with corrected block types
        """
        new_surface_map = copy(self.surface_map)
        water_blocks = [8,9]
        lava_blocks = [10,11]
        for i in range(self.x_length):
            for j in range(self.z_length):
                block = self.surface_map[i][j]
                block_type = level.blockAt(self.to_real_x(i), block.height, self.to_real_z(j))
                if block_type in water_blocks:
                    #print("Found Water")
                    block.is_water = True
                elif block_type in lava_blocks:
                    #print("Found Lava")
                    block.is_lava = True
                new_surface_map[i][j] = block
        return new_surface_map

    def calc_steepness(self):
        """
        calculate steepness of the blocks in the surface_map.
            Accomplished by taking an average of the 8 surrounding blocks and
            finding the difference between the curr block and the average
        :return: new_surface_map filled with calculated steepness data
        """
        new_surface_map = copy(self.surface_map)
        directions = [(0, 0), (1, 0), (1, 1), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1)]
        for i in range(self.x_length):
            for j in range(self.z_length):
                neighbors = [self.add((i, j), connection) for connection in directions]
                neighbors_heights = [self.surface_map[n[0]][n[1]].height for n in neighbors if 0 <= n[0] < self.x_length and 0 <= n[1] < self.z_length]
                avg_height = float(sum(neighbors_heights) / len(neighbors_heights))
                new_surface_map[i][j].steepness = int(round(abs(self.surface_map[i][j].height - avg_height)))
        return new_surface_map

    @staticmethod
    def add(x, y):
        if x is None:
            return y
        if y is None:
            return x
        return x[0] + y[0], x[1] + y[1]

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

    def get_height(self, x, z, level):
        """
        Find the first ground block before air using a binary search.
        :param x: x-coord to the block
        :param z: z-coord to the block
        :param level: level object which stores the worlds blocks and block data
        :return: height (y-value) of the first ground block before air.
        """
        if self.y_start > self.y_end:
            top = self.y_start + 60
            bottom = self.y_end - 60
            y = self.y_start - (abs(self.y_start - self.y_end) / 2)  # Start at halfway.
        else:
            top = self.y_end + 60
            bottom = self.y_start - 60
            y = self.y_end - (abs(self.y_start - self.y_end)/2)  # Start at halfway.
        found = False
        while not found:
            block = level.blockAt(self.to_real_x(x), y, self.to_real_z(z))
            if block in surface_blocks:
                neighbour_below = level.blockAt(self.to_real_x(x), y - 1, self.to_real_z(z))
                if neighbour_below not in surface_blocks:
                    return y-1
                else:
                    top = y
                    y = y - int(round(float(y - bottom)/2))
            else:
                neighbour_above = level.blockAt(self.to_real_x(x), y + 1, self.to_real_z(z))
                if neighbour_above in surface_blocks:
                    return y
                else:
                    bottom = y
                    y = y + int(round(float(top - y) / 2))

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

    def visualize_yards(self):
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
                           "W" if self.surface_map[i][j].is_water == True else
                           "L" if self.surface_map[i][j].is_lava == True else
                           " ")
            row.append("|")
            print("  ".join(row))
        print("| " + "".join([" + " for _ in range(self.x_length)]) + " |")

    def visualize_heights(self):
        """
        Visualize the surface.surface_map by printing out heights
        :return: void
        """
        print("Surface Looks Like: \n")
        print("| " + "".join([" + " for _ in range(self.x_length)]) + " |")
        for j in range(self.z_length):
            row = ["|"]
            for i in range(self.x_length):
                row.append(str(self.surface_map[i][j].height))
            row.append("|")
            print("  ".join(row))
        print("| " + "".join([" + " for _ in range(self.x_length)]) + " |")

    def visualize_steepness(self):
        """
        Visualize the surface.surface_map by printing out steepness values
        :return: void
        """
        print("Surface Looks Like: \n")
        print("| " + "".join([" + " for _ in range(self.x_length)]) + " |")
        for j in range(self.z_length):
            row = ["|"]
            for i in range(self.x_length):
                row.append(str(self.surface_map[i][j].steepness))
            row.append("|")
            print("  ".join(row))
        print("| " + "".join([" + " for _ in range(self.x_length)]) + " |")
