from math import floor

from backtrader.dataseries import TimeFrame
from pybit.unified_trading import HTTP, WebSocket

from .bybit_broker import BybitBroker
from .bybit_feed import BybitData
from .enums import *


class BybitStore(object):
    _GRANULARITIES = {
        (TimeFrame.Minutes, 1): KLINE_INTERVAL_1MINUTE,
        (TimeFrame.Minutes, 3): KLINE_INTERVAL_3MINUTE,
        (TimeFrame.Minutes, 5): KLINE_INTERVAL_5MINUTE,
        (TimeFrame.Minutes, 15): KLINE_INTERVAL_15MINUTE,
        (TimeFrame.Minutes, 30): KLINE_INTERVAL_30MINUTE,
        (TimeFrame.Minutes, 60): KLINE_INTERVAL_1HOUR,
        (TimeFrame.Minutes, 120): KLINE_INTERVAL_2HOUR,
        (TimeFrame.Minutes, 240): KLINE_INTERVAL_4HOUR,
        (TimeFrame.Minutes, 360): KLINE_INTERVAL_6HOUR,
        (TimeFrame.Minutes, 720): KLINE_INTERVAL_12HOUR,
        (TimeFrame.Days, 1): KLINE_INTERVAL_1DAY,
        (TimeFrame.Weeks, 1): KLINE_INTERVAL_1WEEK,
        (TimeFrame.Months, 1): KLINE_INTERVAL_1MONTH,
    }

    def __init__(self, api_key, api_secret, coin_target, testnet=False, category="spot", accountType="UNIFIED"):
        self.bybit_session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet)
        self.bybit_socket = WebSocket(api_key=api_key, api_secret=api_secret, testnet=testnet, channel_type="private")

        self.coin_target = coin_target  # USDT
        self.category = category  # Unified account: spot, linear, option. Normal account: linear, inverse.
        self.accountType = accountType  # Unified account: UNIFIED (trade spot/linear/options), CONTRACT(trade inverse)
                                        # Classic account: CONTRACT, SPOT
        self.symbols = []  # symbols

        self._cash = 0
        self._value = 0
        self.get_balance()

        self._step_size = {}
        self._min_order = {}
        self._tick_size = {}

        self._broker = BybitBroker(store=self)
        self._data = None
        self._datas = {}

    def _format_value(self, value, step):
        precision = step.find('1') - 1
        if precision > 0:
            return '{:0.0{}f}'.format(float(value), precision)
        return floor(int(value))
        
    def cancel_open_orders(self, symbol):
        return self.bybit_session.cancel_all_orders(category=self.category, symbol=symbol)

    def cancel_order(self, symbol, order_id):
        return self.bybit_session.cancel_order(category=self.category, symbol=symbol, orderId=order_id)
    
    def create_order(self, symbol, side, type, size, price):
        params = dict()
        if type != ORDER_TYPE_MARKET:
            params.update({
                'price': self.format_price(symbol, price)
            })
        if type == ORDER_TYPE_MARKET:
            params.update({
                'marketUnit': 'baseCoin'
            })

        return self.bybit_session.place_order(
            category=self.category,  # (string): Unified account: spot, linear, option. Normal account: linear, inverse.
            symbol=symbol,           # (string): Symbol name
            side=side,               # (string): Buy, Sell
            orderType=type,          # (string): Market, Limit
            qty=self.format_quantity(symbol, size),  # (string): Order quantity
            **params)

    def format_price(self, symbol, price):
        return self._format_value(price, self._tick_size[symbol])
    
    def format_quantity(self, symbol, size):
        return self._format_value(size, self._step_size[symbol])

    def get_asset_balance(self, asset):
        w = self.bybit_session.get_wallet_balance(accountType=self.accountType)  # wallet_balance
        balance = {}
        if w and 'result' in w and w['result'] and 'list' in w['result'] and w['result']['list']:
            for _coin in w['result']['list'][0]['coin']:
                balance[_coin['coin']] = {"free": _coin['availableToWithdraw'],
                                          "usdValue": _coin['usdValue'],
                                          "locked": _coin['locked'], }
        if asset in balance.keys():
            return float(balance[asset]['free']), float(balance[asset]['locked'])
        else:
            return 0, 0

    def get_symbol_balance(self, symbol):
        """Get symbol balance in symbol"""
        balance = 0
        try:
            symbol = symbol[0:len(symbol)-len(self.coin_target)]
            balance, locked = self.get_asset_balance(symbol)
        except Exception as e:
            print("Error:", e)
        return balance, symbol  # float(balance['locked'])

    def get_balance(self, ):
        """Balance in USDT for example - in coin target"""
        free, locked = self.get_asset_balance(self.coin_target)
        self._cash = free
        self._value = free + locked

    def getbroker(self):
        return self._broker

    def getdata(self, **kwargs):  # timeframe, compression, start_date=None, LiveBars=True
        symbol = kwargs['dataname']
        tf = self.get_interval(kwargs['timeframe'], kwargs['compression'])
        self.symbols.append(symbol)
        self.get_filters(symbol=symbol)
        if symbol not in self._datas:
            self._datas[f"{symbol}{tf}"] = BybitData(store=self, **kwargs)  # timeframe=timeframe, compression=compression, start_date=start_date, LiveBars=LiveBars
        return self._datas[f"{symbol}{tf}"]
        
    def get_filters(self, symbol):
        i = self.bybit_session.get_instruments_info(category=self.category, symbol=symbol)  # symbol_info
        if i and 'result' in i and i['result'] and 'list' in i['result'] and i['result']['list']:
            self._step_size[symbol] = i['result']['list'][0]['lotSizeFilter']['basePrecision']
            self._min_order[symbol] = i['result']['list'][0]['lotSizeFilter']['minOrderQty']
            self._tick_size[symbol] = i['result']['list'][0]['priceFilter']['tickSize']

    def get_interval(self, timeframe, compression):
        return self._GRANULARITIES.get((timeframe, compression))

    def get_symbol_info(self, symbol):
        return self.bybit_session.get_instruments_info(category=self.category, symbol=symbol)

    def stop_socket(self):
        # self.bybit_session.stop()  # not implemented
        pass
