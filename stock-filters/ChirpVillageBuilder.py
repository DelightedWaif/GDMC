from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import utilityFunctions
from random import randrange, uniform

from ChirpVillage import BuildPlaneFinder, Builder

import os

inputs = (
    ('Build Chirp Village', 'label'),
    ('Material1', alphaMaterials.StoneBricks),
    ('Creator: Chirp Nets', 'label'),
)


def perform(level, box, options):
    # filename = os.getcwd() + default_path + 'ghast.schematic'
    # build_from_schematic(x=box.minx, y=box.miny, z=box.minz,
    #                      filename=filename, level=level, box=box, options=options)
    # BasicBuilding(level, box)
    building = Builder.Building()
    building.construct(level, box)

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
    # set cursor to middle of scematic
    cursorPosn = (x-w_offset, y, z-z_offset)
    blocksIDs = range(level.materials.id_limit)
    level.copyBlocksFrom(schematic, BoundingBox(
        (0, 0, 0), (width, height, depth)), cursorPosn, blocksToCopy=blocksIDs)
