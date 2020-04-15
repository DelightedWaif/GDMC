# coding=utf-8
"""
    Box.py
    BoundingBox Class
        Used for Mock class of pymclevel.box.BoundingBox
    Author: Chirp Nets
    © 2020
"""


class BoundingBox(object):

    def __init__(self, minx, miny, minz, maxx, maxy, maxz):
        self.minx = minx
        self.miny = miny
        self.minz = minz
        self.maxx = maxx
        self.maxy = maxy
        self.maxz = maxz
