# coding=utf-8
"""
    YardGenerator.py
        Used for generating yards with building lots and pathway doors
    Author: Chirp Nets
    © 2020
"""
if __name__ != "__main__":
    import utilityFunctions

from Surface import Surface
from RandUtils import lehmer_2, rand_range
from Block import Block
from copy import copy


class YardGenerator(object):

    # CONSTANTS
    MIN_YARD_SIZE = (16, 16)
    MAX_BUILDING_AREA = 100
    MIN_BUILDING_AREA = 50

    def __init__(self, level, box, surface):
        print("YardGenerator.__init__")
        # CA CONFIG
        self.iter_num = 5
        self.death_limit = 4
        self.birth_limit = 3

        self.level = level
        self.seed = level.RandomSeed
        self.x_start = box.minx
        self.z_start = box.minz
        self.x_end = box.maxx
        self.z_end = box.maxz
        self.x_length = abs(self.x_end - self.x_start)
        self.z_length = abs(self.z_end - self.z_start)
        self.surface = surface
        self.partitions = self.get_partitions()
        self.building_coords = []
        self.door_blocks = []
        self.building_door_blocks = []

    def get_partitions(self):
        """
        Partition the surface surface_map into chunks no smaller than MIN_YARD_SIZE
            - Uses a randomized binary space partition-like approach to splitting the current segment
            - We split x axis first, then for each x segment we split the z axis to ensure unequal grid cells
        :returns: a list of tuples of coords to the corners of each partition chunk (eg. [((x_start,z_start),(x_end,z_end))])
        """
        print("get_partitions")
        partitions = []
        x_splits = self.calc_x_splits()
        curr_x = 3
        for i, x_split in enumerate(x_splits):
            z_splits = self.calc_z_splits(i)
            curr_z = 3
            for z_split in z_splits:
                partitions.append(((curr_x, curr_z), (x_split-3, z_split-3)))
                curr_z = z_split
            curr_x = x_split
        return partitions

    def calc_x_splits(self):
        """
        Calculate vertical splitting lines for the surface map
            - Uses a depth first algorithm to create splitting lines.
        :returns: a list of x values to specify the vertical splitting line.
        """
        print("calc_x_splits")
        partition_lines = []
        segments = []
        if self.x_length/2 > self.MIN_YARD_SIZE[0]:
            segments.append((self.x_length, 0))
        while len(segments) > 0:
            top, bottom = segments.pop()
            # NOTE: x_start+bottom and x_end+top are used as seeds to ensure different divisors
            rand_div = float(rand_range(self.x_start + bottom, self.x_end + top, 230, 170)) / 100
            curr = bottom + (int(round(float(top - bottom) / rand_div)))
            partition_lines.append(curr)
            if (top - curr + 1) / 2 > self.MIN_YARD_SIZE[0]:
                segments.append((top, curr + 1))
            if (curr - bottom) / 2 > self.MIN_YARD_SIZE[0]:
                segments.append((curr, bottom))
        partition_lines.append(self.x_length)
        partition_lines.sort()
        return partition_lines

    def calc_z_splits(self, offset):
        """
        Calculate horizontal splitting lines for the segment of surface map specified by offset (vertical offset)
            - Uses a depth first algorithm to create splitting lines.
        :params offset: vertical offset within the surface map. This is defined by the x_split
        :returns: a list of z values to specify the horizontal splitting lines for the current vertical offset
                within the surface map.
        """
        print("calc_z_splits")
        partition_lines = []
        segments = []
        if self.z_length/2 > self.MIN_YARD_SIZE[1]:
            segments.append((self.z_length, 0))
        while len(segments) > 0:
            top, bottom = segments.pop()
            # NOTE: z_start+bottom and z_end+top are used as seeds to ensure different divisors
            rand_div = float(rand_range(self.z_start + bottom + offset, self.z_end + top + offset, 230, 170)) / 100
            curr = bottom + (int(round(float(top - bottom) / rand_div)))
            partition_lines.append(curr)
            if (top - curr + 1) / 2 > self.MIN_YARD_SIZE[1]:
                segments.append((top, curr + 1))
            if (curr - bottom) / 2 > self.MIN_YARD_SIZE[1]:
                segments.append((curr, bottom))
        partition_lines.append(self.z_length)
        partition_lines.sort()
        return partition_lines

    def generate_yards(self):
        """
        Generate yards, building lots, path doors, building doors and place them within the self.surface member
        :returns: void (sets self.surface)
        """
        print("generate_yards")
        new_surface = copy(self.surface)
        probability_generate_yard = 0.90  # Chance of partition being a yard
        for p in self.partitions:
            partition_prob = float((lehmer_2(lehmer_2(self.seed, p[1][0] - p[0][0]), p[1][1] - p[0][1])) % 100) / 100
            if partition_prob < probability_generate_yard:
                new_surface = self.run_ca_on_partition(new_surface, p)
                new_surface = self.generate_building_lots(new_surface, p)
                new_surface = self.generate_building_door_blocks(new_surface, p)
                new_surface = self.generate_door_blocks(new_surface, p)
        self.surface = new_surface

    def run_ca_on_partition(self, new_surface, partition):
        """
        Run the yard generating cellular automata within the partition on the surface.
        :returns: Surface obj new_surface that CA has ran on
        """
        print("run_ca_on_partition")
        new_surface = self.init_surface(new_surface, partition[0][0], partition[1][0], partition[0][1], partition[1][1])
        new_surface = self.do_ca(new_surface, partition[0][0], partition[1][0], partition[0][1], partition[1][1])
        return new_surface

    def init_surface(self, new_surface, x_start, x_end, z_start, z_end):
        """
        Initialize the new_surface to have random blocks set to type Block.YARD to initialize the CA
        :params new_surface: a Surface object to be modified and returned
        :params x_start, x_end, z_start, z_end: the current partition bounds
        :returns: a modified new_surface that has been initialized for CA iterations
        """
        print("init_surface")
        probability_spawning_yard_block = 0.40
        for i in range(x_start, x_end):
            for j in range(z_start, z_end):
                block_probability = float((lehmer_2(lehmer_2(self.seed, i), j)) % 100) / 100
                if block_probability < probability_spawning_yard_block and not new_surface.surface_map[i][j].is_lava:
                    new_surface.surface_map[i][j].type = Block.YARD
        return new_surface

    def do_ca(self, new_surface, x_start, x_end, z_start, z_end):
        """
        Run the CA on the new_surface within the partition
        :params new_surface: a Surface object to be modified and returned
        :params x_start, x_end, z_start, z_end: the current partition bounds
        :returns: a modified new_surface that has been modified by the CA
        """
        print("do_ca")
        for _ in range(self.iter_num):
            new_surface = self.do_iteration_step(new_surface, x_start, x_end, z_start, z_end)

        #draw
        if __name__ != "__main__":
            for i in range(x_start, x_end):
                for j in range(z_start, z_end):
                    if self.surface.surface_map[i][j].type == Block.YARD and self.count_neighbours(i,j, x_start,x_end,z_start,z_end,Block.UNASSIGNED) > 1:
                        utilityFunctions.setBlock(self.level, (85, 0), self.surface.to_real_x(i), self.surface.surface_map[i][j].height+1, self.surface.to_real_z(j))

        return new_surface

    def do_iteration_step(self, new_surface, x_start, x_end, z_start, z_end):
        """
        Run a single CA iteration step on the new_surface within the partition
        :params new_surface: a Surface object to be modified and returned
        :params x_start, x_end, z_start, z_end: the current partition bounds
        :returns: a modified new_surface that has been modified by the CA iteration step
        """
        print("do_iteration_step")
        for i in range(x_start, x_end):
            for j in range(z_start, z_end):
                num_alive_neighbours = self.count_neighbours(i, j, x_start, x_end, z_start, z_end, Block.YARD)
                if self.surface.surface_map[i][j].type == Block.YARD:
                    if num_alive_neighbours < self.death_limit:
                        new_surface.surface_map[i][j].type = Block.UNASSIGNED  # cell dies
                    else:
                        new_surface.surface_map[i][j].type = Block.YARD  # cell stays alive
                else:
                    if num_alive_neighbours > self.birth_limit and not new_surface.surface_map[i][j].is_lava:
                        new_surface.surface_map[i][j].type = Block.YARD  # cell dies
                    else:
                        new_surface.surface_map[i][j].type = Block.UNASSIGNED  # cell stays alive
        return new_surface

    def count_neighbours(self, x, z, x_start, x_end, z_start, z_end, type):
        """
        Counts the number of neighbours of type type rooted at x,z within the given partition
        :params x, z: root cell coords
        :params x_start, x_end, z_start, z_end: the current partition bounds
        :params type: the Block.type of neighbour we are looking for
        :returns: count of the neighbours of type type
        """
        print("count_neighbours")
        count = 0
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                neighbour_x = x + i
                neighbour_z = z + j
                if neighbour_x < x_start or neighbour_z < z_start or neighbour_x >= x_end or neighbour_z >= z_end:
                    if type == Block.UNASSIGNED:
                        count = count + 1
                elif self.surface.surface_map[neighbour_x][neighbour_z].type == type:
                    count = count + 1
        return count

    def generate_building_lots(self, new_surface, partition):
        """
        Generate a single building lot within the yard within the given partition
        :params new_surface: a post CA Surface object to be modified and returned
        :params x_start, x_end, z_start, z_end: the current partition bounds
        :returns: a modified new_surface that has the building lots set
            (also fills the self.building_coords list with tuples of coords to the corners of the building)
        """
        print("generate_buildings")

        x_start, x_end, z_start, z_end = self.get_partition_bounds(partition)

        # Random Growth Rate for the building lots
        growth_1 = rand_range(x_start, z_start, 2, 1)
        growth_2 = 3 - growth_1

        # starting in center of yard
        corners = ((x_end - ((x_end - x_start) / 2), (z_end - (z_end - z_start) / 2)),
                   (x_end - ((x_end - x_start) / 2), (z_end - (z_end - z_start) / 2)))

        # extend corners down and right until not valid, then back up one extension step
        while self.are_valid_corners(new_surface, corners):
            corners = ((corners[0][0] - growth_1, corners[0][1] - growth_2), (corners[1][0], corners[1][1]))
        corners = ((corners[0][0] + growth_1, corners[0][1] + growth_2), (corners[1][0], corners[1][1]))

        # extend corners up and left until not valid, then back up one extension step
        while self.are_valid_corners(new_surface, corners):
            corners = ((corners[0][0], corners[0][1]), (corners[1][0] + growth_2, corners[1][1] + growth_1))
        corners = ((corners[0][0], corners[0][1]), (corners[1][0] - growth_2, corners[1][1] - growth_1))

        building_lot_area = abs(corners[1][0] - corners[0][0]) * abs(corners[1][1] - corners[0][1])
        if building_lot_area > YardGenerator.MIN_BUILDING_AREA:
            # if building lot of good size add to building coords and mark blocks in cells as buildings
            self.building_coords.append(corners)
            for i in range(corners[0][0], corners[1][0]):
                for j in range(corners[0][1], corners[1][1]):
                    new_surface.surface_map[i][j].type = Block.BUILDING
        else:
            # else erase the entire yard as it is not able to hold a valid building lot
            for i in range(x_start, x_end):
                for j in range(z_start, z_end):
                    new_surface.surface_map[i][j].type = Block.UNASSIGNED
        return new_surface

    @staticmethod
    def are_valid_corners(new_surface, corners):
        """
        Check to see if the building lot defined by corners is valid (within a yard and area under MAX_BUILDING_AREA)
        :params new_surface: a post CA Surface object to be modified and returned
        :params corners: the current building lot corners
        :returns: a bool to indicate validness of the corners (is the building lot within the yard)
        """
        print("are_valid_corners")
        valid = True
        if (corners[1][0] - corners[0][0]) * (corners[1][1] - corners[0][1]) > YardGenerator.MAX_BUILDING_AREA:
            # if building lot area is too big, building lot also not valid
            return False

        for i in range(corners[0][0], corners[1][0]):
            for j in range(corners[0][1], corners[1][1]):
                valid = valid and new_surface.surface_map[i][j].type == Block.YARD
        return valid

    def generate_door_blocks(self, new_surface, partition):
        """
        Generate a single door block on the edge of the yard within the partition
        :params new_surface: a post CA Surface object to be modified and returned
        :params x_start, x_end, z_start, z_end: the current partition bounds
        :returns: a modified new_surface that has the door cells set
            (also fills the self.doors list with coords to the door block)
        """
        print("generate_door_blocks")

        x_start, x_end, z_start, z_end = self.get_partition_bounds(partition)

        option = rand_range(x_start, z_start, 3, 0)  # pick one of four options for door placement
        curr = (x_end - ((x_end - x_start) / 2), (z_end - ((z_end - z_start) / 2)))  # set curr to center of yard
        if new_surface.surface_map[curr[0]][curr[1]].type == Block.UNASSIGNED:
            # if center block is not a yard, return
            return new_surface

        # OPTION 1: look for yard edge to the left
        if option == 0:
            while new_surface.surface_map[curr[0]][curr[1]].type != Block.UNASSIGNED:
                curr = (curr[0]+1, curr[1])
            curr = (curr[0] - 1, curr[1])

        # OPTION 2: look for yard edge to the right
        elif option == 1:
            while new_surface.surface_map[curr[0]][curr[1]].type != Block.UNASSIGNED:
                curr = (curr[0]-1, curr[1])
            curr = (curr[0] + 1, curr[1])

        # OPTION 3: look for yard edge upward
        elif option == 2:
            while new_surface.surface_map[curr[0]][curr[1]].type != Block.UNASSIGNED:
                curr = (curr[0], curr[1]+1)
            curr = (curr[0], curr[1]-1)

        # OPTION 4: look for yard edge downward
        elif option == 3:
            while new_surface.surface_map[curr[0]][curr[1]].type != Block.UNASSIGNED:
                curr = (curr[0], curr[1]-1)
            curr = (curr[0], curr[1]+1)
        self.door_blocks.append(curr)
        new_surface.door_blocks.append(curr)
        new_surface.surface_map[curr[0]][curr[1]].type = Block.DOOR
        return new_surface

    def generate_building_door_blocks(self, new_surface, partition):
        """
        Generate a single door block on the edge of the building lot
        :params new_surface: a post CA Surface object to be modified and returned
        :params x_start, x_end, z_start, z_end: the current partition bounds
        :returns: a modified new_surface that has the building door cells set
            (also fills the self.building_doors list with coords to the door block)
        """
        print("generate_building_door_blocks")

        x_start, x_end, z_start, z_end = self.get_partition_bounds(partition)

        option = rand_range(x_start, z_start, 3, 0)  # pick one of four options for door placement
        curr = (x_end - ((x_end - x_start) / 2), (z_end - ((z_end - z_start) / 2)))  # set curr to center of yard
        if new_surface.surface_map[curr[0]][curr[1]].type != Block.BUILDING:
            # if center block is not a building lot, return
            return new_surface

        # OPTION 1: look for yard edge to the left
        if option == 0:
            while self.within_bounds(new_surface, curr) and new_surface.surface_map[curr[0]][curr[1]].type != Block.YARD:
                curr = (curr[0]+1, curr[1])
            curr = (curr[0] - 1, curr[1])

        # OPTION 2: look for yard edge to the right
        elif option == 1:
            while self.within_bounds(new_surface, curr) and new_surface.surface_map[curr[0]][curr[1]].type != Block.YARD:
                curr = (curr[0]-1, curr[1])
            curr = (curr[0] + 1, curr[1])

        # OPTION 3: look for yard edge upward
        elif option == 2:
            while self.within_bounds(new_surface, curr) and new_surface.surface_map[curr[0]][curr[1]].type != Block.YARD:
                curr = (curr[0], curr[1]+1)
            curr = (curr[0], curr[1]-1)

        # OPTION 4: look for yard edge to the downward
        elif option == 3:
            while self.within_bounds(new_surface, curr) and new_surface.surface_map[curr[0]][curr[1]].type != Block.YARD:
                curr = (curr[0], curr[1]-1)
            curr = (curr[0], curr[1]+1)
        self.building_door_blocks.append(curr)
        new_surface.surface_map[curr[0]][curr[1]].type = Block.BUILDING_DOOR
        return new_surface

    @staticmethod
    def within_bounds(new_surface, curr):
        return 0 < curr[0] < len(new_surface.surface_map) and 0 < curr[1] < len(new_surface.surface_map[curr[0]])

    @staticmethod
    def get_partition_bounds(partition):
        return partition[0][0], partition[1][0], partition[0][1], partition[1][1]


if __name__ == "__main__":
    # MOCKS FOR TESTING ONLY
    from Mocks.Level import Level
    from Mocks.Box import BoundingBox

    level = Level()
    box = BoundingBox(25, 70, 25, 225, 80, 225)
    surface = Surface(level, box)
    yard_generator = YardGenerator(level, box, surface)
    yard_generator.generate_yards()
    surface = yard_generator.surface
    surface.visualize_yards()
    surface.visualize_heights()
    surface.visualize_steepness()
