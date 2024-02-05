import datetime as dt

from collections import defaultdict, deque
from math import copysign

from backtrader.broker import BrokerBase
from backtrader.order import Order, OrderBase
from backtrader.position import Position
from .enums import *


class BybitOrder(OrderBase):
    def __init__(self, owner, data, exectype, bybit_order, side, size, price):
        self.owner = owner
        self.data = data
        self.exectype = exectype
        self.ordtype = self.Buy if side == SIDE_BUY else self.Sell
        
        # Market order price is zero
        if self.exectype == Order.Market:
            self.size = size
            self.price = None
        else:
            self.size = size
            self.price = price
        # !!!! {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1613709150486009088', 'orderLinkId': '1613709150486009089'}, 'retExtInfo': {}, 'time': 1707105121370}
        self.bybit_order = bybit_order['result']
        self.bybit_order['time'] = bybit_order['time']
        self.bybit_order['symbol'] = self.data._name

        super(BybitOrder, self).__init__()
        self.accept()


class BybitBroker(BrokerBase):
    _ORDER_TYPES = {
        Order.Limit: ORDER_TYPE_LIMIT,
        Order.Market: ORDER_TYPE_MARKET,
        Order.Stop: ORDER_TYPE_STOP_LOSS,
        Order.StopLimit: ORDER_TYPE_STOP_LOSS_LIMIT,
    }

    def __init__(self, store):
        super(BybitBroker, self).__init__()

        self.notifs = deque()
        self.positions = defaultdict(Position)

        self.startingcash = self.cash = 0  # Стартовые и текущие свободные средства по счету
        self.startingvalue = self.value = 0  # Стартовая и текущая стоимость позиций

        self.open_orders = list()
    
        self._store = store
        self._store.bybit_socket.order_stream(self._handle_user_socket_message)

    def start(self):
        self.startingcash = self.cash = self.getcash()  # Стартовые и текущие свободные средства по счету. Подписка на позиции для портфеля/биржи
        self.startingvalue = self.value = self.getvalue()  # Стартовая и текущая стоимость позиций

    def _execute_order(self, order, date, executed_size, executed_price, executed_value, executed_comm):
        order.execute(
            date,
            executed_size,
            executed_price,
            0, executed_value, executed_comm,
            0, 0.0, 0.0,
            0.0, 0.0,
            0, 0.0)
        pos = self.getposition(order.data, clone=False)
        pos.update(copysign(executed_size, order.size), executed_price)

    def _handle_user_socket_message(self, msg):
        """https://bybit-exchange.github.io/docs/v5/websocket/private/position"""
        # print(msg)
        # !!!! {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1613710659319764224', 'orderLinkId': '1613710659319764225'}, 'retExtInfo': {}, 'time': 1707105301238}
        # {'topic': 'order', 'id': '112927970-22008-17722138290', 'creationTime': 1707105301240,
        # 'data': [{'category': 'spot', 'symbol': 'ETHUSDT', 'orderId': '1613710659319764224', 'orderLinkId': '1613710659319764225', 'blockTradeId': '', 'side': 'Buy', 'positionIdx': 0, 'orderStatus': 'New',
        # 'cancelType': 'UNKNOWN', 'rejectReason': 'EC_NoError', 'timeInForce': 'GTC', 'isLeverage': '0', 'price': '2175.53', 'qty': '0.00062', 'avgPrice': '', 'leavesQty': '0.00062', 'leavesValue': '1.3488286',
        # 'cumExecQty': '0.00000', 'cumExecValue': '0.0000000', 'cumExecFee': '0', 'orderType': 'Limit', 'stopOrderType': '', 'orderIv': '', 'triggerPrice': '0.00', 'takeProfit': '0.00', 'stopLoss': '0.00',
        # 'triggerBy': '', 'tpTriggerBy': '', 'slTriggerBy': '', 'triggerDirection': 0, 'placeType': '', 'lastPriceOnCreated': '2291.34', 'closeOnTrigger': False, 'reduceOnly': False, 'smpGroup': 0,
        # 'smpType': 'None', 'smpOrderId': '', 'slLimitPrice': '0.00', 'tpLimitPrice': '0.00', 'marketUnit': '', 'createdTime': '1707105301237', 'updatedTime': '1707105301239', 'feeCurrency': ''}]}

        # {'topic': 'order', 'id': '112927970-22008-17725759811', 'creationTime': 1707108121276,
        # 'data': [{'category': 'spot', 'symbol': 'ETHUSDT', 'orderId': '1613734315479536896', 'orderLinkId': '1613734315479536897', 'blockTradeId': '', 'side': 'Buy', 'positionIdx': 0, 'orderStatus': 'Filled',
        # 'cancelType': 'UNKNOWN', 'rejectReason': 'EC_NoError', 'timeInForce': 'IOC', 'isLeverage': '0', 'price': '0', 'qty': '0.00094', 'avgPrice': '2294.41', 'leavesQty': '0.00000', 'leavesValue': '0.0647002',
        # 'cumExecQty': '0.00094', 'cumExecValue': '2.1567454', 'cumExecFee': '0.00000094', 'orderType': 'Market', 'stopOrderType': '', 'orderIv': '', 'triggerPrice': '0.00', 'takeProfit': '0.00', 'stopLoss': '0.00',
        # 'triggerBy': '', 'tpTriggerBy': '', 'slTriggerBy': '', 'triggerDirection': 0, 'placeType': '', 'lastPriceOnCreated': '2294.41', 'closeOnTrigger': False, 'reduceOnly': False, 'smpGroup': 0, 'smpType': 'None',
        # 'smpOrderId': '', 'slLimitPrice': '0.00', 'tpLimitPrice': '0.00', 'marketUnit': 'baseCoin', 'createdTime': '1707108121272', 'updatedTime': '1707108121274', 'feeCurrency': 'ETH'}]}
        if 'topic' in msg and msg['topic'] == 'order' and 'data' in msg:
            for d in msg['data']:
                if d['symbol'] in self._store.symbols:
                    # print(f"msg: {d['symbol']}")
                    # print(len(self.open_orders))
                    for o in self.open_orders:
                        # print("o:", o)
                        # print("o.bybit_order:", o.bybit_order)
                        if o.bybit_order['orderId'] == d['orderId']:
                            if d['orderStatus'] in [ORDER_STATUS_FILLED, ORDER_STATUS_PARTIALLY_FILLED]:
                                _dt = dt.datetime.fromtimestamp(int(d['updatedTime']) / 1000)
                                executed_size = float(d['cumExecQty'])
                                executed_price = float(d['avgPrice'])
                                executed_value = float(d['cumExecValue'])
                                executed_comm = float(d['cumExecFee'])
                                # print(_dt, executed_size, executed_price)
                                self._execute_order(o, _dt, executed_size, executed_price, executed_value, executed_comm)
                            self._set_order_status(o, d['orderStatus'])

                            if o.status not in [Order.Accepted, Order.Partial]:
                                self.open_orders.remove(o)
                            self.notify(o)
        else: print(msg)
    
    def _set_order_status(self, order, bybit_order_status):
        if bybit_order_status == ORDER_STATUS_CANCELED:
            order.cancel()
        elif bybit_order_status == ORDER_STATUS_EXPIRED:
            order.expire()
        elif bybit_order_status == ORDER_STATUS_FILLED:
            order.completed()
        elif bybit_order_status == ORDER_STATUS_PARTIALLY_FILLED:
            order.partial()
        elif bybit_order_status == ORDER_STATUS_REJECTED:
            order.reject()

    def _submit(self, owner, data, side, exectype, size, price):
        type = self._ORDER_TYPES.get(exectype, ORDER_TYPE_MARKET)
        symbol = data._name
        bybit_order = self._store.create_order(symbol, side, type, size, price)
        order = BybitOrder(owner, data, exectype, bybit_order, side, size, price)
        if order.status == Order.Accepted:
            self.open_orders.append(order)
        self.notify(order)
        return order

    def buy(self, owner, data, size, price=None, plimit=None,
            exectype=None, valid=None, tradeid=0, oco=None,
            trailamount=None, trailpercent=None,
            **kwargs):
        return self._submit(owner, data, SIDE_BUY, exectype, size, price)

    def cancel(self, order):
        order_id = order.bybit_order['orderId']
        symbol = order.bybit_order['symbol']
        self._store.cancel_order(symbol=symbol, order_id=order_id)
        
    def format_price(self, value):
        return self._store.format_price(value)

    def get_asset_balance(self, asset):
        return self._store.get_asset_balance(asset)

    def getcash(self):
        self.cash = self._store._cash
        return self.cash

    def get_notification(self):
        if not self.notifs:
            return None

        return self.notifs.popleft()

    def getposition(self, data, clone=True):
        pos = self.positions[data._dataname]
        if clone:
            pos = pos.clone()
        return pos

    def getvalue(self, datas=None):
        self.value = self._store._value
        return self.value

    def notify(self, order):
        self.notifs.append(order)

    def sell(self, owner, data, size, price=None, plimit=None,
             exectype=None, valid=None, tradeid=0, oco=None,
             trailamount=None, trailpercent=None,
             **kwargs):
        return self._submit(owner, data, SIDE_SELL, exectype, size, price)
