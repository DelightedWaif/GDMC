from collections import deque
from Block import Block
from YardGenerator import YardGenerator


class PathGenerator:
    def __init__(self, surface):
        self.surface = surface
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
        while current != start:
            # find next in path
            x, z = current
            block = self.surface.surface_map[x][z]
            block.type = Block.PATH
            current = self.add(current, path[current])


# test code
if __name__ == "__main__":
    from Mocks.Box import BoundingBox
    from Mocks.Level import Level
    level = Level()
    box = BoundingBox(0, 0, 50 , 50)
    yard_generator = YardGenerator(level, box)
    yard_generator.generate_yards()
    surface = yard_generator.surface
    print(surface.door_blocks)
    path_generator = PathGenerator(surface)
    path_generator.generate_paths()
    surface.visualize()
