from collections import deque
from Block import Block
from YardGenerator import YardGenerator
import utilityFunctions
from Biomes import BlockUtils


class PathGenerator:
    def __init__(self, surface, level):
        self.surface = surface
        self.level = level
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    @staticmethod
    def subtract(x, y):
        if x is None:
            return y
        if y is None:
            return x
        return x[0] - y[0], x[1] - y[1]

    @staticmethod
    def add(x, y):
        if x is None:
            return y
        if y is None:
            return x
        return x[0] + y[0], x[1] + y[1]

    # Returns whether the
    def block_is_free(self, node):
        x, z = node
        block = self.surface.surface_map[x][z]
        return block.type == Block.UNASSIGNED or block.type == Block.PATH or block.type == Block.DOOR

    # Returns whether the cell is within the grid
    def block_in_grid(self, block):
        return 0 <= block[0] < self.surface.x_length and 0 <= block[1] < self.surface.z_length

    def get_block_neighbors(self, block):
        neighbors = [self.add(block, connection) for connection in self.directions]
        neighbors = filter(self.block_in_grid, neighbors)
        neighbors = filter(self.block_is_free, neighbors)
        return neighbors

    def generate_paths(self):
        doors = self.surface.door_blocks
        while len(doors) > 0:
            start = doors.pop(0)
            for goal in doors:
                self.find_paths_BFS(start, goal)

    def find_paths_BFS(self, start, end):
        path = {}
        cell_queue = deque()
        cell_queue.append(start)
        path[start] = None
        while len(cell_queue) > 0:
            current = cell_queue.popleft()
            if current == end:
                break
            for next in self.get_block_neighbors(current):
                if next not in path:
                    cell_queue.append(next)
                    path[next] = self.subtract(current, next)

        # Draw paths
        current = self.add(end, path[end])
        direction = path[end]
        while current != start:
            # find next in path
            x, z = current
            block = self.surface.surface_map[x][z]
            block.type = Block.PATH
            # # If path his moving horiziontally, try to widen it by adding blocks above and below it
            # if (direction == (-1,0) or direction == (1,0)):
            #     path_edges = [(x, z-1), (x, z+1)]
            # # If path his moving vertically, try to widen it by adding blocks to the left and to the right of it
            # elif (direction == (0,-1) or direction == (0,1)):
            #     path_edges = (x-1, z), (x+1, z)
            path_edges = [(x, z-1), (x, z+1), (x-1, z), (x+1, z)]
            path_edges = filter(self.block_in_grid, path_edges)
            path_edges = filter(self.block_is_free, path_edges)
            for edge in path_edges:
                block = self.surface.surface_map[edge[0]][edge[1]]
                block.type = Block.PATH
                level_block = BlockUtils.get_road_block(block.biome_id)
                utilityFunctions.setBlock(self.level, level_block, self.surface.to_real_x(block.x), block.height, self.surface.to_real_z(block.z))
                above = block.height + 1
                while self.level.blockAt(self.surface.to_real_x(block.x), above, self.surface.to_real_z(block.z)) != 0:
                    utilityFunctions.setBlock(self.level, (0, 0), self.surface.to_real_x(block.x), above, self.surface.to_real_z(block.z))
                    above += 1

            level_block = BlockUtils.get_road_block(block.biome_id)
            utilityFunctions.setBlock(self.level, level_block, self.surface.to_real_x(block.x), block.height, self.surface.to_real_z(block.z))
            above = block.height + 1
            while self.level.blockAt(self.surface.to_real_x(x), above, self.surface.to_real_z(z)) != 0:
                utilityFunctions.setBlock(self.level, (0, 0), self.surface.to_real_x(block.x), above, self.surface.to_real_z(block.z))
                above += 1
            current = self.add(current, path[current])
            direction = path[current]


# test code
if __name__ == "__main__":
    from Mocks.Box import BoundingBox
    from Mocks.Level import Level
    level = Level()
    box = BoundingBox(0, 0, 75 , 75)
    yard_generator = YardGenerator(level, box)
    yard_generator.generate_yards()
    surface = yard_generator.surface
    print(surface.door_blocks)
    path_generator = PathGenerator(surface, level)
    path_generator.generate_paths()
    surface.visualize()
