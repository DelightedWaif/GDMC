from Mocks.Box import BoundingBox
from Mocks.Level import Level
from Surface import Surface
from collections import deque
from Block import Block


class PathGenerator:
    def __init__(self, surface):
        self.surface = surface
        self.path = None

    @staticmethod
    def subtract(x, y):
        return x[0] - y[0], x[1] - y[1]

    @staticmethod
    def add(x, y):
        return x[0] + y[0], x[1] + y[1]

    def in_bounds(self, node):
        return 0 <= node[0] < self.surface.x_length and 0 <= node[1] < self.surface.z_length

    def passable(self, node):
        x, z = node
        block = self.surface.surface_map[x][z]
        return block.type == Block.UNASSIGNED or block.type == Block.PATH

    #               right    left    down   up
    connections = [(1, 0), (-1, 0), (0,1), (0,-1)]

    def find_neighbors(self, node):
        neighbors = [self.add(node, connection) for connection in self.connections]
        # don't use this for diagonals:
        if (node[0] + node[1]) % 2:
            neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    goal = (0,0)
    start = (3,0)

    def breadth_first_search(self, start, end):
        frontier = deque()
        frontier.append(start)
        path = {}
        path[start] = None
        while len(frontier) > 0:
            current = frontier.popleft()
            if current == end:
                break
            for next in self.find_neighbors(current):
                if next not in path:
                    frontier.append(next)
                    path[next] = current - next
        self.path = path
        return path

    def draw_paths(self):


def main():
    level = Level()
    box = BoundingBox(0, 0, 50 , 50)
    surface = Surface(level, box)
    surface.populate_surface_map()
    surface.visualize()

main()