# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:51:54 2017

@author: Johan Steunenberg
"""

import os
import v20

class OandaSession:
    def __init__(self, oanda_key = None, url = None):
        if oanda_key is None:
            self.key = os.environ['OANDA_KEY']
        else:
            self.key = oanda_key
        if url is None:
            self.url = "api-fxpractice.oanda.com"
        else:
            self.url = url
        self.api = v20.Context(self.url, 443, token=self.key)
      
        self.accounts = {}

