# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:45:44 2017

@author: Johan <kontakt@steunenberg.de>
"""

#from simplev20.oandasession import OandaSession
from simplev20.oandaaccount import OandaAccount

import unittest

class ShortStub:
    units = -50.0
class LongStub:
    units = 100.0
class V20PositionStub:
    """
    Stub class to mimick positions in OandaAccount 
    without opening a real session
    """
    def __init__(self, instrument = "EUR_USD"):
        self.instrument = instrument
        self.long = LongStub()
        self.short = ShortStub()
    
class V20SessionStub:
    """
    Stub class to mimick the v20 api usage in OandaAccount 
    without opening a real session
    """
    def __init__(self):
        self.account = self
        self.balance = 1000.0
        self.positions = [V20PositionStub()]
        
    def get(self, someparam):
        return self
    
        
class TestOandaAccount(unittest.TestCase):
    """
    The test assumes the availability of a valid oanda key in the
    environment variable OANDA_KEY. The key should be valid for 
    a test account
    """
    def setUp(self):
        self.api = V20SessionStub()
        self.testid = 'BLAFASEL'
        self.account = OandaAccount(self.api, self.testid)
        
    def test_create(self):
        """
        An simple test, asserting that the setup of the test
        and the constructor of the account work fine
        """
        self.assertEqual(self.api, self.account.api)
        self.assertEqual(self.testid, self.account.account_id)
        
    def test_balance(self):
        balance = self.account.get_balance()
        self.assertEqual(balance, 1000.0)
        
    def test_get_instruments_with_open_positions(self):
        instruments =self.account.get_instruments_with_open_positions()
        self.assertEqual(len(instruments), 1)
        self.assertEqual(instruments[0], "EUR_USD")
        
    def test_get_position(self):
        self.assertEqual(self.account.get_position("EUR_USD"), 50.0)
        self.assertEqual(self.account.get_position("EUR_USD", 'net'), 50.0)
        self.assertEqual(self.account.get_position("EUR_USD", 'long'), 100.0)
        self.assertEqual(self.account.get_position("EUR_USD", 'short'), -50.0)
        self.assertEqual(self.account.get_position("EUR_GBP"), 0.0)
#        self.assertRaises(ValueError, self.account.get_position("EUR_USD", 'nett'))
        
        
unittest.main()
