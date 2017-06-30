# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:45:44 2017

@author: Johan <kontakt@steunenberg.de>
"""

#from simplev20.oandasession import OandaSession
from simplev20.oandaaccount import OandaAccount

from collections import defaultdict
import unittest

class ShortStub:
    units = -50.0
class LongStub:
    units = 100.0
class V20OrderStub:
    """
    Stub class to mimick trades in OandaAccount 
    without opening a real session
    """
    def __init__(self, tradeid, order_type, price, anid):
        self.tradeID = tradeid
        self.type = order_type
        self.id = anid
        self.price = price
        self.closed = defaultdict(lambda:1)
        self.status = 0
    def close(self, account_id, order_id):
        if self.closed[order_id] == 1:
            self.closed[order_id] = 0
            self.status = 200
        else:
            self.status = 0
        return self
        
class V20TradeStub:
    """
    Stub class to mimick trades in OandaAccount 
    without opening a real session
    """
    def __init__(self, ticker, anid, position):
        self.instrument = ticker
        self.id = anid
        self.currentUnits = position
        
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
        ticker = "EUR_USD"
        self.trades = [V20TradeStub(ticker, 4711, -1000.0)]
        self.orders = [V20OrderStub(4711, 'TAKE_PROFIT', 1.1234, 4715)]
        self.trade = V20OrderStub(0, 'LIMIT', 1.1234, 4719)
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
        self.assertRaises(ValueError, self.account.get_position, ticker='EUR_USD', long_short='nett')

    def test_get_trades(self):
        # account.get_trades returns a dictionary with 
        # key = ticker, val = list of trades
        trades = self.account.get_trades()
        self.assertEqual(len(trades), 1)
        self.assertIsInstance(trades, dict)
        dollartrades = trades['EUR_USD']
        trade1 = dollartrades[0]
        self.assertEqual(trade1['ticker'], 'EUR_USD')
        self.assertEqual(trade1['id'], 4711)
        self.assertEqual(trade1['position'], -1000.0)


    def test_get_orders(self):
        orders = self.account.get_orders('EUR_USD')  
        self.assertEqual(len(orders), 1)
        self.assertIsInstance(orders, list)
        order = orders[0]
        self.assertIsInstance(order, dict)
        self.assertEqual(order['type'], 'TAKE_PROFIT')
        self.assertEqual(order['units'], -1000.00)
        self.assertEqual(order['price'], 1.1234)
        orders = self.account.get_orders('EUR_USD', 'ALL')  
        self.assertEqual(len(orders), 1)
        orders = self.account.get_orders('EUR_USD', 'TAKE_PROFIT')  
        self.assertEqual(len(orders), 1)
        orders = self.account.get_orders('EUR_USD', 'WHATEVER')  
        self.assertEqual(len(orders), 0)
        
    # close an existing order
    def test_close_order(self):
        self.assertEqual(self.account.close_order(4719), 200)
        # can't close the same order twice
        self.assertNotEqual(self.account.close_order(4719), 200)
        
    # next steps
    # open a market order
    def test_market_order(self):
        ticker = 'EUR_USD'
        self.assertEqual(self.account.market_order(ticker, 1), 200)
    # open a limit order
        
        
unittest.main()
