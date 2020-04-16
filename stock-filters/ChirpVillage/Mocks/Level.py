# coding=utf-8
"""
    Level.py
    Level Class
        Used for Mock class of pymclevel.MCLevel
    Author: Chirp Nets
    © 2020
"""

from random import randrange


class Level(object):

    def __init__(self, x_min=0, y_min=0, z_min=0, x_max=300, y_max=254, z_max=300):
        self.RandomSeed = 2523870351887443968
        self.x_min = x_min
        self.y_min = y_min
        self.z_min = z_min
        self.x_max = x_max
        self.y_max = y_max
        self.z_max = z_max
        self.world = self.init_world()

    def init_world(self):
        """
        Initialize the world with stone or air blocks at random height (30->254)
        :return: initialized 3d world filled with generated data
        """
        world = []
        for i in range(self.x_max):
            j_column = []
            for j in range(self.z_max):
                height = randrange(60, 80)
                # add river down center
                if j == self.z_max-self.z_min:
                    j_column.append([0 if h >= height else 8 for h in range(self.y_max)])
                # add lava down quarter
                elif j == (self.z_max -self.z_min)/2:
                    j_column.append([0 if h >= height else 10 for h in range(self.y_max)])
                else:
                    j_column.append([0 if h >= height else 1 for h in range(self.y_max)])
            world.append(j_column)
        return world

    def blockAt(self, x, y, z):
        """
        Fetch the block that is at the coords
        :param x, y, z: x, y, z coords to the block required
        :return: block at the x, y, z coords in the 3d world matrix member
        """
        return self.world[x][z][y]
