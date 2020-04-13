from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from BasicBuilding import BasicBuilding
from Surface import Surface
import utilityFunctions
from random import randrange, uniform
from ChirpVillage import BuildPlaneFinder, Builder
import BlockUtils
import os

inputs = (
    ('Build Chirp Village', 'label'),
    ('Creator: Chirp Nets', 'label'),
)


def perform(level, box, options):
    surface = Surface(level, box)
    BlockUtils.calculate_biomes_on_surface(level, surface)
    # calculateHeightMapAdv(level, surface)
    # calculateSteepnessMap(surface)
    # calculateWaterPlacement(level, surface)


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
