# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:39:43 2017

@author: Johan  <kontakt@steunenberg.de>
"""

class OandaAccount:
    """
    An account object has a pointer to the calling session's api and 
    an ID.
    Every call on the object retrieves the information directly from 
    OANDA, the only information in memory is the session.api and the id
    """
    def __init__(self, api, account_id):
        self.api = api
        self.account_id = account_id

    def __acc(self):
        """
        gets the actual information from the account.
        base method for all public methods
        """
        return self.api.account.get(self.account_id).get('account')
        
    def get_balance(self):
        """
        returns the actual account balance
        """
        return self.__acc().balance

    def get_instruments_with_open_positions(self):
        """
        Retrieves a list with the instruments we have open positions for
        """
        ins = []
        for pos in self.__acc().positions:
            ins.append(pos.instrument)
        return ins

    def get_position(self, ticker, long_short='net'):
        for pos in self.__acc().positions:
            ins = pos.instrument
            if ins == ticker:
                long = pos.long.units
                short = pos.short.units
                if long_short == 'net':
                    return long + short
                elif long_short == 'long':
                    return long
                elif long_short == 'short':
                    return short
                else:
                    msg = 'Parameter long_short on method OandaAccount.get_position'
                    msg += ' must be either "long", "short" or "net"'
                    raise ValueError(msg)
                
            
        return 0.0
