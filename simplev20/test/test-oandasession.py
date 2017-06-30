# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:51:54 2017

@author: Johan Steunenberg <kontakt@steunenberg.de>
"""
from simplev20.oandasession import OandaSession

import unittest
import os

class TestOandaSession(unittest.TestCase):
    """
    The test assumes the availability of a valid oanda key in the
    environment variable OANDA_KEY. The key should be valid for 
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
        self.assertIsNotNone(self.session)
        
    def test_init_loads_accounts(self):
        """
        tests the initalization
        """
        self.assertIsNotNone(self.session)
        self.assertGreater(len(self.session.accounts), 0)
        self.assertIsNotNone(self.session.primary)
        
    def test_has_accounts(self):
        """
        tests the getters that get the accounts and the primary account
        set in the constructor
        """
        self.assertIsNotNone(self.session.get_primary_account())
        self.assertGreater(len(self.session.get_accounts()), 0)
       
    def test_get_account_from_id(self):
        primary = self.session.get_primary_account()
        test = self.session.get_account(primary.account_id)
        self.assertEqual(primary, test)
        
    def test_get_default_curve(self):
        ticker = 'EUR_USD'
        curve = self.session.get_curve(ticker=ticker)
        self.assertEqual(len(curve.keys()), 3)
        self.assertEqual(len(curve['mid']), 500)
        self.assertEqual(ticker, curve['ticker'])
        self.assertEqual('D', curve['granularity'])
        
    def test_get_defined_curve(self):
        ticker = 'EUR_USD'
        count=1000
        granularity='S10'
        price='BMA'
        curve = self.session.get_curve(ticker=ticker, count=count, granularity=granularity, price=price)
        self.assertEqual(len(curve.keys()), 5)
        self.assertEqual(len(curve['mid']), count)
        self.assertEqual(ticker, curve['ticker'])
        self.assertEqual(granularity, curve['granularity'])
        
        

unittest.main()

