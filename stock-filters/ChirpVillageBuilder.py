# coding=utf-8
"""
    ChirpVillageBuilder.py
    Main Entry point for the ChirpVillageFilter
    Author: Chirp Nets
    © 2020
"""


from pymclevel import MCSchematic, MCLevel, BoundingBox
from Surface import Surface
from ChirpVillage import Builder
from ChirpVillage.Biomes import BlockUtils
from ChirpVillage.YardGenerator import YardGenerator
from ChirpVillage.PathGeneration import PathGenerator
from ChirpVillage.RandUtils import rand_range

inputs = (
    ('Build Chirp Village', 'label'),
    ('Creator: Chirp Nets', 'label'),
)


def perform(level, box, options):
    # Yard Generation
    surface = Surface(level, box)
    yard_generator = YardGenerator(level, box, surface)
    yard_generator.generate_yards()
    surface = yard_generator.surface

    # Biome Adaptibility
    BlockUtils.calculate_biomes_on_surface(level, surface)

    # Path Generation
    path_generator = PathGenerator(surface, level)
    path_generator.generate_paths()
    # Building Generation
    # building = Builder.BasicBuilding()
    for door, building_lot in zip(yard_generator.building_door_blocks, yard_generator.building_coords):
        rand =  rand_range(door[0], door[1], 100, 0)
        print(rand)
        print((building_lot[0], building_lot[1]))
        print(door)
        if rand < 30:
            building = Builder.BasicBuilding()
        elif rand < 60:
            building = Builder.MultiStoryBuilding()
        else:
            building = Builder.DecoratedBuilding()
        building.construct(level, (building_lot[0], building_lot[1]), (surface.to_real_x(door[0]), surface.to_real_z(door[1])), surface)


# This is a slightly modified version of a schematic reader function found at:
# http://www.brightmoore.net/mcedit-filters-1/blockschematicswapper
def build_from_schematic(x, y, z, filename, level, box, options):
    schematic = MCSchematic(filename=filename)
    width = schematic.Width
    depth = schematic.Length
    height = schematic.Height
    w_offset = width >> 1
    z_offset = depth >> 1
    cursorPosn = (x - w_offset, y, z - z_offset)  # set cursor to middle of scematic
    blocksIDs = range(level.materials.id_limit)
    level.copyBlocksFrom(schematic, BoundingBox(
        (0, 0, 0), (width, height, depth)), cursorPosn, blocksToCopy=blocksIDs)
