# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:51:54 2017

@author: Johan Steunenberg <kontakt@steunenberg.de>
"""

from simplev20.oandaaccount import OandaAccount

import os
import pandas as pd
import v20

class OandaSession:
    """
    An OandaSession gives access to accounts, curves, streams
    On init the accounts associated with the login are loaded
    """
    price_type_dict = {'M': 'mid', 'B': 'bid', 'A': 'ask'}

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

        try:
            accountlist = self.api.account.list().get('accounts')
        except:
            msg = 'One of the parameters key ({}) or url ({}) seems to be wrong'
            raise ValueError(msg.format(self.key, self.url))
            
        for a in accountlist:
            self.accounts[a.id] = OandaAccount(self.api, a.id)
            acc = self.api.account.get(a.id)
            acc = acc.get('account')
            if acc.alias == 'Primary':
                self.primary = self.accounts[a.id]
 
    def get_accounts(self):
        return self.accounts

    def get_account(self, account_id):
        return self.accounts[account_id]
        
    def get_primary_account(self):
        return self.primary

    def __get_raw_curve(self, ticker, granularity='D', count=None, price='M'):
        if count is None:
            response = self.api.instrument.candles(instrument=ticker, 
                                                   granularity=granularity,
                                                   price=price)
        else:
            response = self.api.instrument.candles(instrument=ticker, 
                                                   granularity=granularity, 
                                                   count=count,
                                                   price=price)
        return response
        
    def __get_candle_line( self, time, prices, volume, complete):
        if prices is None:
            raise ValueError('empty candle returned')
            
        d = prices.dict()
            
        result = {}
        result['time'] = time
        result['open'] = float(d['o'])
        result['high'] = float(d['h'])
        result['low'] = float(d['l'])
        result['close'] = float(d['c'])
        result['volume'] = volume
        result['complete'] = complete

        return result
        
    def get_curve(self, ticker, granularity='D', count=None, price='M'):
        # depending on the price parameter, result is a dictionary
        # of one up to three dataframes
        result = {}
        # bt to get there I need a dictionary with one up to three  
        # lists of dictionaries with raw values
        intermediate = {}

        # prepare the intermediate dictionary for the price tags
        for p in price:
            tag = OandaSession.price_type_dict[p]
            intermediate[tag] = []
        possible_prices = 'BMA'
        
        # now get and check the raw data
        response = self.__get_raw_curve(ticker, granularity, count, price)
        if response.status != 200:
            print(response.body)
            msg = 'HTTP Status {}, message: {}'.format(response.status, response.body)
            raise RuntimeError(msg)

        # the needed values are in the candles
        candles = response.get('candles', 200)
        for candle in candles:
            # get the generic values from the candle
            time = candle.time
            volume = candle.volume
            complete = candle.complete
            for p in possible_prices:
                if price.find(p) >= 0:
                    tag = OandaSession.price_type_dict[p]
                    if p == 'M':
                        intermediate[tag].append(self.__get_candle_line(time, candle.mid, volume, complete))
                    elif p == 'B': 
                        intermediate[tag].append(self.__get_candle_line(time, candle.bid, volume, complete))
                    elif p == 'A': 
                        intermediate[tag].append(self.__get_candle_line(time, candle.ask, volume, complete))
                    else:
                        raise ValueError('Wondering what happened as the only valid values are B, M or A')
            

        for k, v in intermediate.items():
            df = pd.DataFrame(v)
            # make time the index and a date time column
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            result[k] = df
        result['ticker'] = ticker
        result['granularity'] = granularity               
        return result

#session = OandaSession()