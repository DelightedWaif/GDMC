from Block import Block


class Surface(object):

    def __init__(self, x_start, z_start, x_end, z_end):
        self.x_start = x_start
        self.z_start = z_start
        self.x_end = x_end
        self.z_end = z_end
        self.x_length = x_end - x_start
        self.z_length = z_end - z_start
        self.surface_map = self.init_surface_map()
        self.door_blocks = []

    def init_surface_map(self):
        surface_map = []
        for i in range(self.x_length):
            row = []
            for j in range(self.z_length):
                row.append(Block(i, j, 0))
            surface_map.append(row)
        return surface_map

    def to_real_x(self, x):
        return self.x_start + x

    def to_real_z(self, z):
        return self.z_start + z
