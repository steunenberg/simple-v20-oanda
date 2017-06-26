# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:51:54 2017

@author: Johan Steunenberg <kontakt@steunenberg.de>
"""

from simplev20.oandaaccount import OandaAccount

import os
import v20

class OandaSession:
    """
    An OandaSession gives access to accounts, curves, streams
    On init the accounts associated with the login are loaded
    """
    def __init__(self, oanda_key = None, url = None):
        if oanda_key is None:
            self.key = os.environ['OANDA_KEY']
        else:
            self.key = oanda_key
        if url is None:
            self.url = "api-fxpractice.oanda.com"
        else:
            self.url = url
        self.session = v20.Context(self.url, 443, token=self.key)
      
        self.accounts = {}

        try:
            accountlist = self.session.account.list().get('accounts')
        except:
            msg = 'One of the parameters key ({}) or url ({}) seems to be wrong'
            raise ValueError(msg.format(self.key, self.url))
            
        for a in accountlist:
            self.accounts[a.id] = OandaAccount(self.session, a.id)
            acc = self.session.account.get(a.id)
            acc = acc.get('account')
            if acc.alias == 'Primary':
                self.primary = self.accounts[a.id]
 
    def get_accounts(self):
        return self.accounts

    def get_account(self, account_id):
        return self.accounts[account_id]
        
    def get_primary_account(self):
        return self.primary

session = OandaSession()