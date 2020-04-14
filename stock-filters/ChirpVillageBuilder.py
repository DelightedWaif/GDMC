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

inputs = (
    ('Build Chirp Village', 'label'),
    ('Creator: Chirp Nets', 'label'),
)


def perform(level, box, options):
    yard_generator = YardGenerator(level, box)
    yard_generator.generate_yards()
    surface = yard_generator.surface
    BlockUtils.calculate_biomes_on_surface(level, surface)
    path_generator = PathGenerator(surface, level)
    path_generator.generate_paths()
    building = Builder.BasicBuilding()
    building.construct(level, ((surface.to_surface_x(box.minx), surface.to_surface_z(box.minz)), (surface.to_surface_x(box.maxx), surface.to_surface_z(box.maxz))), surface)


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
