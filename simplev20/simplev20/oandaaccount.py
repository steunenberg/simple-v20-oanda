# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:39:43 2017

@author: Johan  <kontakt@steunenberg.de>
"""
from simplev20.oandaorder import OandaOrder

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
        Retrieves a list with the instruments we have open 
        positions for in the current account
        """
        ins = []
        for pos in self.__acc().positions:
            ins.append(pos.instrument)
        return ins

    def get_position(self, ticker, long_short='net'):
        """
        Retrieves the open position for a specific instrument 
        in the current account
        """
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

    def get_trades(self):
        """
        Retrieves the open trades in the current account
        """
        result = {}
        trades = self.__acc().trades
        # get relevant trade ids and the current positions
        for trade in trades:
            ticker = trade.instrument
            trade_id = trade.id
            position = trade.currentUnits
            if ticker not in result.keys():
                result[ticker] = []
            result[ticker].append({'ticker':ticker, 'id':trade_id, 'position': position})
        return result
        
    def get_orders(self, ticker, order_type='ALL'):
        trade_positions = {}
        result = []
        acc = self.__acc()
        trades = acc.trades
        orders = acc.orders
        # get relevant trade ids and the current positions
        for trade in trades:
            if trade.instrument == ticker:
                trade_positions[trade.id] = trade.currentUnits
        # and get the orders
        for order in orders:
            if order.tradeID in trade_positions.keys():
                _type = order.type
                if (order_type == 'ALL' or order_type == _type):
                    d = {}
                    d['type'] = _type
                    d['price'] = order.price
                    d['units'] = trade_positions[order.tradeID]
                    result.append(OandaOrder(order_id=order.id, 
                                             order_type=_type, 
                                             price=order.price, 
                                             units=trade_positions[order.tradeID],
                                             trade_id=order.tradeID))
        return result
        
    # close an order
    # api.trade.close('101-004-6211473-001', 28) gives response
    # check status!!!
    # in this case
    # self.api.trade.close(self.account_id, order_id)
    def close_order(self, order_id):
        response = self.api.trade.close(self.account_id, order_id)
        status = response.status
        return status
        
    def market_order(self, ticker, units):
        response = self.api.order.market(self.account_id, ticker, units)
        status = response.status
        return status
        
    def get_available_instruments(self):
        response = self.api.account.instruments(self.account_id)
        instruments = response.get("instruments", "200")
        return sorted([i.name for i in instruments])
    