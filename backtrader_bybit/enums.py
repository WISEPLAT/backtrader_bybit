from enum import Enum

KLINE_INTERVAL_1MINUTE = '1'
KLINE_INTERVAL_3MINUTE = '3'
KLINE_INTERVAL_5MINUTE = '5'
KLINE_INTERVAL_15MINUTE = '15'
KLINE_INTERVAL_30MINUTE = '30'
KLINE_INTERVAL_1HOUR = '60'
KLINE_INTERVAL_2HOUR = '120'
KLINE_INTERVAL_4HOUR = '240'
KLINE_INTERVAL_6HOUR = '360'
KLINE_INTERVAL_12HOUR = '720'
KLINE_INTERVAL_1DAY = 'D'
KLINE_INTERVAL_1WEEK = 'W'
KLINE_INTERVAL_1MONTH = 'M'

SIDE_BUY = 'Buy'
SIDE_SELL = 'Sell'

ORDER_TYPE_LIMIT = 'Limit'
ORDER_TYPE_MARKET = 'Market'
ORDER_TYPE_STOP_LOSS = 'StopLoss'
ORDER_TYPE_STOP_LOSS_LIMIT = 'Stop'

ORDER_STATUS_NEW = 'New'
ORDER_STATUS_PARTIALLY_FILLED = 'PartiallyFilled'
ORDER_STATUS_FILLED = 'Filled'
ORDER_STATUS_CANCELED = 'Cancelled'
ORDER_STATUS_REJECTED = 'Rejected'
ORDER_STATUS_EXPIRED = 'Expired'  # no such type in bybit
