#!/usr/bin/env python

"""
Central API module
"""

## IMPORTS #####################################################################

from canada_post import PROD, Auth
from canada_post.service.shipping import (CreateShipment, VoidShipment)
from canada_post.service.rating import (GetRates)

## CLASSES #####################################################################

class CanadaPostAPI(object):
    def __init__(self, customer_number, username, password, contract_number="",
                 dev=PROD):
        self.auth = Auth(customer_number, username, password, contract_number,
                         dev)
        self.get_rates = GetRates(self.auth)
        self.create_shipment = CreateShipment(self.auth)
        self.void_shipment = VoidShipment(self.auth)
