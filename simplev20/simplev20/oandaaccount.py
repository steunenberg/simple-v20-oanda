# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:39:43 2017

@author: Johan  <kontakt@steunenberg.de>
"""

class OandaAccount:
    """
    An account object has a pointer to the calling session and 
    an ID.
    Every call on the object retrieves the information directly from 
    OANDA, the only information in memory is the session and the id
    """
    def __init__(self, session, account_id):
        self.session = session
        self.account_id = account_id

    def __acc(self):
        """
        gets the actual information from the account.
        base method for all public methods
        """
        return self.session.account.get(self.account_id).get('account')
        
    def get_balance(self):
        """
        returns the actual account balance
        """
        return self.__acc().balance

