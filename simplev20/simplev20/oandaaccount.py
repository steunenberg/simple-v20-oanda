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


