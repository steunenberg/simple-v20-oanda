# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 20:12:57 2017

@author: Johan
"""

from simplev20.oandaorder import OandaOrder

import unittest

class TestOandaOrder(unittest.TestCase):
    
    def setUp(self):
        self.order = OandaOrder(order_id='4567', 
                                order_type='STOP', 
                                price=1.23245, 
                                units=10)

    def test_create(self):
        """
        An simple test, asserting that the setup of the test
        and the constructor of the account work fine
        """
        self.assertIsInstance(self.order, OandaOrder)
        
    def test_price_property(self):
        self.assertEqual(self.order.price, 1.23245)
        self.order.price += 0.001
        self.assertEqual(self.order.price, 1.23345)
        self.assertRaises(ValueError, setattr,  self.order, 'price', -1.)
        
    def test_units_property(self):
        self.assertEqual(self.order.units, 10)
        self.order.units += 10
        self.assertEqual(self.order.units, 20)
        
    def test_type_property(self):
        self.assertEqual(self.order.type, 'STOP')
        self.assertRaises(AttributeError, setattr,  self.order, 'type', 'HURRAH')
        
    def test_id_property(self):
        self.assertEqual(self.order.id, '4567')
        self.assertRaises(AttributeError, setattr,  self.order, 'id', 4711)
        
unittest.main()        