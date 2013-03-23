#!/usr/bin/env python

"""
Configuration module for the API. This defines whether to use the development
or production credentials/urls (and what the credentials are).
"""

## IMPORTS #####################################################################

## CONSTANTS ###################################################################

VERSION = "0.0.4-1"
DEV = "DEV"
PROD = "PROD"

_auth = None

## FUNCTIONS ###################################################################

def set_credentials(customer_number, username, password, dev=PROD):
    if _auth is None:
        _auth = Auth(customer_number, username, password, dev)

## CLASSES #####################################################################

class Auth(object):
    USERNAME = {
        DEV: "",
        PROD: "",
        }
    PASSWORD = {
        DEV: "",
        PROD: "",
        }

    def __init__(self, customer_number="", username="", password="",
                 contract_number="", dev=PROD):
        self.dev = dev
        self.debug = dev == DEV
        self.customer_number = customer_number
        self.contract_number = contract_number
        self.USERNAME[dev] = username
        self.PASSWORD[dev] = password

    @property
    def username(self):
        return self.USERNAME[self.dev]

    @property
    def password(self):
        return self.PASSWORD[self.dev]




