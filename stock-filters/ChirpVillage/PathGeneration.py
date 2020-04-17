from collections import deque
from Block import Block
from YardGenerator import YardGenerator
import utilityFunctions
from Biomes import BlockUtils
from Surface import Surface


class PathGenerator:
    def __init__(self, surface, level):
        self.surface = surface
        self.level = level
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Subtract two tuples as if they were vectors
    @staticmethod
    def subtract(x, y):
        if x is None:
            return y
        if y is None:
            return x
        return x[0] - y[0], x[1] - y[1]

    # Add two tuples together as if they were vectors
    @staticmethod
    def add(x, y):
        if x is None:
            return y
        if y is None:
            return x
        return x[0] + y[0], x[1] + y[1]

    # Returns whether the block is free
    def block_is_free(self, node):
        x, z = node
        block = self.surface.surface_map[x][z]
        return block.type == Block.UNASSIGNED or block.type == Block.PATH or block.type == Block.DOOR and not block.is_lava

    # Returns whether the cell is within the grid
    def block_in_grid(self, block):
        return 0 <= block[0] < self.surface.x_length and 0 <= block[1] < self.surface.z_length

    # Finds neighbors of block
    def get_block_neighbors(self, block):
        neighbors = [self.add(block, connection) for connection in self.directions]
        neighbors = filter(self.block_in_grid, neighbors)
        neighbors = filter(self.block_is_free, neighbors)
        return neighbors

    # Run the BFS to generate paths
    def generate_paths(self):
        doors = self.surface.door_blocks
        while len(doors) > 0:
            start = doors.pop(0)
            for goal in doors:
                self.find_paths_BFS(start, goal)

    # Run a BFS to connect the start and end points
    def find_paths_BFS(self, start, end):
        path = {}
        cell_queue = [start]
        path[start] = None
        while len(cell_queue) > 0:
            current = cell_queue.pop(0)
            if current == end:
                break
            for next in self.get_block_neighbors(current):
                if next not in path:
                    cell_queue.append(next)
                    path[next] = self.subtract(current, next)

        # Draw paths
        current = self.add(end, path[end])
        direction = path[end]
        prev = end
        while current != start:
            # find next in path
            x, z = current
            block = self.surface.surface_map[x][z]
            previous_block = self.surface.surface_map[prev[0]][prev[1]]
            block.type = Block.PATH
            steepness = previous_block.height - block.height
            new_height = block.height
            if steepness > 1:
                if steepness > 4:
                    new_height = self.surface.surface_map[prev[0]][prev[1]].height
                else:
                    new_height = self.surface.surface_map[prev[0]][prev[1]].height - 1
            elif previous_block.height - block.height < -1:
                new_height = self.surface.surface_map[prev[0]][prev[1]].height + 1
            block.height = new_height
            # If path is moving horizontally, try to widen it by adding blocks above and below it
            if direction == (-1,0) or direction == (1,0):
                path_edges = [(x, z-1), (x, z+1)]
            # If path is moving vertically, try to widen it by adding blocks to the left and to the right of it
            else:
                path_edges = [(x-1, z), (x+1, z)]
            path_edges = filter(self.block_in_grid, path_edges)
            path_edges = filter(self.block_is_free, path_edges)
            for edge in path_edges:
                edge_block = self.surface.surface_map[edge[0]][edge[1]]
                edge_block.type = Block.PATH
                # Set path block in level
                level_block = BlockUtils.get_road_block(edge_block.biome_id)
                bridge_block = BlockUtils.get_bridge_block(edge_block.biome_id)
                if edge_block.is_water:
                    utilityFunctions.setBlock(self.level, bridge_block, self.surface.to_real_x(edge_block.x), new_height, self.surface.to_real_z(edge_block.z))
                else:
                    utilityFunctions.setBlock(self.level, level_block, self.surface.to_real_x(edge_block.x), new_height, self.surface.to_real_z(edge_block.z))
                # Remove all blocks above paths
                above = new_height + 1
                while self.level.blockAt(self.surface.to_real_x(edge_block.x), above, self.surface.to_real_z(edge_block.z)) != 0:
                    utilityFunctions.setBlock(self.level, (0, 0), self.surface.to_real_x(edge_block.x), above, self.surface.to_real_z(edge_block.z))
                    above += 1
            # Set path block in level
            level_block = BlockUtils.get_road_block(block.biome_id)
            bridge_block = BlockUtils.get_bridge_block(block.biome_id)
            if block.is_water:
                utilityFunctions.setBlock(self.level, bridge_block, self.surface.to_real_x(block.x), new_height, self.surface.to_real_z(block.z))
            else:
                utilityFunctions.setBlock(self.level, level_block, self.surface.to_real_x(block.x), new_height, self.surface.to_real_z(block.z))
            above = new_height + 1
            # Remove all blocks above paths
            while self.level.blockAt(self.surface.to_real_x(x), above, self.surface.to_real_z(z)) != 0:
                utilityFunctions.setBlock(self.level, (0, 0), self.surface.to_real_x(block.x), above, self.surface.to_real_z(block.z))
                above += 1
            prev = current
            current = self.add(current, path[current])
            direction = path[current]


# test code
if __name__ == "__main__":
    from Mocks.Box import BoundingBox
    from Mocks.Level import Level
    level = Level()
    box = BoundingBox(0, 0, 0, 75 , 0, 75)
    surface = Surface(level, box)
    yard_generator = YardGenerator(level, box, surface)
    yard_generator.generate_yards()
    surface = yard_generator.surface
    path_generator = PathGenerator(surface, level)
    path_generator.generate_paths()
    surface.visualize()
