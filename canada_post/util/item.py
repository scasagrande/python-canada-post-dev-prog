#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# item.py: Representation of an item in the parcel
##
# © 2014 Steven Casagrande (scasagrande@galvant.ca).
#
# This file is a part of the shipping_manager project.
# Licensed under the AGPL version 3.
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
##

## FEATURES ####################################################################

from __future__ import division

## IMPORTS #####################################################################

import pycountry

## CLASSES #####################################################################

class Item(object):
    """
    The Item class represents an item to be included in the parcel. This 
    contains the relevant customs information such as weight, country of origin,
    and description.
    """
    def __init__(self, num_units = 0, description = '', unit_weight = 0, 
                 unit_value = 0, origin_country = None, origin_province=None):
        self.number_of_units = num_units
        self.description = description
        self.unit_weight = unit_weight
        self.unit_value = unit_value
        self.origin_country = origin_country
        self.origin_province = origin_province
    
    @property
    def number_of_units(self):
        """
        Gets/sets the number of units for this item to be included in the 
        parcel. Valid range is 0 to 9999 inclusive.
        
        :type: `int`
        """
        return self._num_units
    @number_of_units.setter
    def number_of_units(self, newval):
        if not isinstance(newval, int):
            raise TypeError('Number of units must be specified as an integer')
        if (newval < 0) or (newval > 9999):
            raise ValueError('Number of units must be between 0 and 9999 '
                             'inclusive')
        self._num_units = newval
    
    @property
    def description(self):
        """
        Gets/sets the customs description used for this item. Max length is 45
        characters.
        
        :type: `str`
        """
        return self._description
    @description.setter
    def description(self, newval):
        if not isinstance(newval, str):
            raise TypeError('Description must be specified as a string.')
        if len(newval) > 45:
            raise ValueError('Description must be a max of 45 chars long.')
        
        self._description = newval
        
    @property
    def unit_weight(self):
        """
        Gets/sets the unit weight of the item. Weight shall be specified in kg.
        
        Returns a 2.3 formatted string (eg 00.120)
        
        :type: `float`
        :rtype: `str`
        """
        return "%06.3f"%self._unit_weight
    @unit_weight.setter
    def unit_weight(self, newval):
        if not isinstance(newval, float):
            raise TypeError('Unit weight must be specified as a float.')
        if newval < 0:
            raise ValueError('Unit weight must be positive')
        if newval > 99.999:
            raise ValueError('Unit weight must be less than 100kg')
        
        self._unit_weight = newval
        
    @property
    def unit_value(self):
        """
        Gets/sets the unit value fo the item. 
        
        Returns a 5.2 formatted string (eg 00001.20)
        
        :type: `float`
        :rtype: `str`
        """
        return "%08.2f"%self._unit_value
    @unit_value.setter
    def unit_value(self, newval):
        if not isinstance(newval, float):
            raise TypeError('Unit value must be specified as a float.')
        if newval < 0:
            raise ValueError('Unit value must be positive')
        if newval > 99999.99:
            raise ValueError('Unit value must be less than 99999.99')
            
        self._unit_value = newval
        
    @property
    def origin_country(self):
        """
        Gets/sets the country of origin for the item. Returns the 2-character
        country code.
        
        :type: `str`
        """
        return self._origin_country
    @origin_country.setter
    def origin_country(self, newval):
        if not isinstance(newval, str):
            raise TypeError('Country origin must be specified as a string.')
        
        country_codes = []
        for country in pycountry.countries:
            country_codes.append(country.alpha2)
        
        countries = {}
        for country in pycountry.countries:
            countries[country.name] = country.alpha2
        
        if len(newval) is 2:
            if newval.upper() in country_codes:
                self._origin_country = newval.upper()
            else:
                raise ValueError('Not a valid 2-char country code.')
        else:
            self._origin_country = countries[newval]
    
    @property
    def origin_province(self):
        """
        Gets/sets the province of origin for the item. This should be used when
        the country of origin is Canada. Returns the 2-character province code.
        
        :type: `str`
        """
        return self._origin_province
    @origin_province.setter
    def origin_province(self, newval):
        if not isinstance(newval, str):
            raise TypeError('Province origin must be specified as a string.')
            
        province_codes = ['AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON',
                          'PE', 'QC', 'SK', 'YT']
        province_english = ['Alberta', 'British Columbia', 'Manitoba',
                            'New Brunswick', 'Newfoundland',
                            'Northwest Territories', 'Nova Scotia', 'Nunavut',
                            'Ontario', 'Prince Edward Island', 'Québec',
                            'Saskatchewan', 'Yukon']
        if self.origin_country != 'CA':
            #print self.origin_country
            if newval is not None:
                raise ValueError('Setting province origin is only valid if the '
                                 'country origin is Canada.')
            else:
                self._origin_province = None
        else:                            
            if newval.upper() in province_codes:
                self._origin_province = newval.upper()
            elif newval in province_english:
                self._origin_province = province_codes[province_english.index(newval)]
            elif newval.lower() == 'quebec': # To deal with the accents
                self._origin_province = 'QC'
            else:
                raise ValueError('Not a valid province origin')
