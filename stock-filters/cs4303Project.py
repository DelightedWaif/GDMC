from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import utilityFunctions
from CS4303_Buildings.basic_building import BasicBuilding

inputs = (
    ('cs4303', 'label'),
    ('Material1', alphaMaterials.StoneBricks),
    ('Creator: ChirpNets', 'label'),
)


def perform(level, box, options):
    BasicBuilding(level, box)


def construct_building(level, box, type):
    # This is where we build a building
    pass


def construct_pillars(level, box):
    # This is where we build pillars
    pass


def build_paths(level, box):
    # this is where we build paths
    pass
