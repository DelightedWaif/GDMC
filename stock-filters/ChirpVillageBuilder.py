# coding=utf-8
"""
    ChirpVillageBuilder.py
    Main Entry point for the ChirpVillageFilter
    Author: Chirp Nets
    © 2020
"""


from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from BasicBuilding import BasicBuilding
from Surface import Surface
import utilityFunctions
from random import randrange, uniform
from ChirpVillage import BuildPlaneFinder, Builder
import os
from ChirpVillage.Biomes import BlockUtils
from ChirpVillage.YardGenerator import YardGenerator

inputs = (
    ('Build Chirp Village', 'label'),
    ('Creator: Chirp Nets', 'label'),
)


def perform(level, box, options):
<<<<<<< HEAD
    # filename = os.getcwd() + default_path + 'ghast.schematic'
    # build_from_schematic(x=box.minx, y=box.miny, z=box.minz,
    #                      filename=filename, level=level, box=box, options=options)
    # BasicBuilding(level, box)
    surface = Surface(level, box)
=======
    yard_generator = YardGenerator(level, box)
    yard_generator.generate_yards()
    surface = yard_generator.surface

    # calculateHeightMapAdv(level, surface)
    # calculateSteepnessMap(surface)
    # calculateWaterPlacement(level, surface)

>>>>>>> 5054574a15f54d7a2565406bc28825e869c70261
    BlockUtils.calculate_biomes_on_surface(level, surface)
    # calculateHeightMapAdv(level, surface)
    # calculateSteepnessMap(surface)
    # calculateWaterPlacement(level, surface)
    # BasicBuilding(level, box, surface)
    building = Builder.BasicBuilding()
    building.construct(level, ((surface.to_surface_x(box.minx), surface.to_surface_z(box.minz)), (surface.to_surface_x(box.maxx), surface.to_surface_z(box.maxz))), surface)


def build_paths(level, box):
    # this is where we build paths
    pass


# This is a slightly modified version of a schematic reader function found at:
# http://www.brightmoore.net/mcedit-filters-1/blockschematicswapper
def build_from_schematic(x, y, z, filename, level, box, options):
    schematic = MCSchematic(filename=filename)
    width = schematic.Width
    depth = schematic.Length
    height = schematic.Height
    w_offset = width >> 1
    z_offset = depth >> 1
<<<<<<< HEAD
    # set cursor to middle of scematic
    cursorPosn = (x-w_offset, y, z-z_offset)
=======
    cursorPosn = (x - w_offset, y, z - z_offset)  # set cursor to middle of scematic
>>>>>>> 5054574a15f54d7a2565406bc28825e869c70261
    blocksIDs = range(level.materials.id_limit)
    level.copyBlocksFrom(schematic, BoundingBox(
        (0, 0, 0), (width, height, depth)), cursorPosn, blocksToCopy=blocksIDs)
