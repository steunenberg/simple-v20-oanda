# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:45:44 2017

@author: Johan <kontakt@steunenberg.de>
"""

from simplev20.oandasession import OandaSession
from simplev20.oandaaccount import OandaAccount

import unittest
import os

class TestOandaAccount(unittest.TestCase):
    """
    The test assumes the availability of a valid oanda key in the
    environment variable OANDA_KEY. The key should be valid for 
    a test account
    """
    def setUp(self):
        oanda_key = os.environ['OANDA_KEY']
        url = "api-fxpractice.oanda.com"
        self.session = OandaSession(oanda_key, url)
        # TODO: replace the session with a Mock session
        
    def test_create(self):
        """
        An simple test, asserting that the setup of the test
        and the constructor of the account work fine
        """
        testid = 'BLAFASEL'
        account = OandaAccount(self.session, testid)
        self.assertEqual(self.session, account.session)
        self.assertEqual(testid, account.account_id)
        
unittest.main()
