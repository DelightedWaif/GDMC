# coding=utf-8
"""
    ChirpVillageBuilder.py
    Main Entry point for the ChirpVillageFilter
    Author: Chirp Nets
    © 2020
"""


from pymclevel import MCSchematic, MCLevel, BoundingBox
from ChirpVillage.Surface import Surface
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
    print("RUNNING CHIRP VILLAGE GENERATOR!! ")
    # Yard Generation
    surface = Surface(level, box)
    yard_generator = YardGenerator(level, box, surface)
    yard_generator.generate_yards()
    surface = yard_generator.surface

    # Uncomment for surface visualization
    # surface.visualize_yards()
    # surface.visualize_heights()
    # surface.visualize_steepness()

    # Path Generation
    path_generator = PathGenerator(surface, level)
    path_generator.generate_paths()

    # Building Generation
    for door, building_lot in zip(yard_generator.building_door_blocks, yard_generator.building_coords):
        rand = rand_range(door[0], door[1], 100, 0)
        if rand < 20:
            building = Builder.BasicBuilding()
        elif rand < 40:
            building = Builder.MultiStoryBuilding()
        elif rand < 60:
            building = Builder.LinearFarmLot()
        elif rand < 80:
            building = Builder.DecoratedBuilding()
        else:
            building = Builder.Church()
        building.construct(level, (building_lot[0], building_lot[1]), (door[0], door[1]), surface)
