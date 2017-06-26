# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:51:54 2017

@author: Johan Steunenberg
"""

from simplev20.oandasession import OandaSession

import unittest
import os

class TestOandaSession(unittest.TestCase):
    """
    The test assumes the availability of a valid oanda key in the
    environment variable OANDA_KEY. Zhe key should be valid for 
    a test account
    """
    def setUp(self):
        oanda_key = os.environ['OANDA_KEY']
        url = "api-fxpractice.oanda.com"
        self.session = OandaSession(oanda_key, url)
        
    def test_setup(self):
        """
        An empty test, asserting that the setup of the test works fine
        """
        self.assertFalse(False)

unittest.main()