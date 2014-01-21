#!/usr/bin/env python

"""
Parcel module
"""

## IMPORTS #####################################################################

from canada_post.util import InfoObject

## CLASSES #####################################################################

class Parcel(InfoObject):
    """
    Represents a Canada Post parcel. Holds things as dimensions, weight,
    tracking number...
    """
    def __init__(self, weight_base=0, length=0, width=0, height=0, 
                 unpackaged=False, **kwargs):
        """
        weight -- kilograms
        length -- the largest dimension, in cm
        width  -- the second largest dimension in cm
        height -- the smallest dimension in cm
        """
        self.weight_base = weight_base
        self.weight = weight_base
        self.length = length
        self.width = width
        self.height = height
        self.unpackaged=unpackaged
        super(Parcel, self).__init__(**kwargs)

    def __unicode__(self):
        return "Parcel {}kg-{}x{}x{}".format(self.weight,
                                             self.length,
                                             self.width,
                                             self.height)
