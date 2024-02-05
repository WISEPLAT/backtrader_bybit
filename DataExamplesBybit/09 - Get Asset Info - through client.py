import backtrader as bt
from backtrader_bybit import BybitStore
from ConfigBybit.Config import Config
from decimal import Decimal

cerebro = bt.Cerebro(quicknotify=True)

cerebro.broker.setcash(100000)  # Setting how much money
cerebro.broker.setcommission(commission=0.0015)  # Set the commission - 0.15% ... divide by 100 to remove %

coin_target = 'USDT'  # the base ticker in which calculations will be performed
symbols = ('BTC', 'ETH', 'BNB')  # tickers for which we will receive data

store = BybitStore(
    api_key=Config.BYBIT_API_KEY,
    api_secret=Config.BYBIT_API_SECRET,
    coin_target=coin_target,
    testnet=False)  # Bybit Storage

client = store  # !!!

asset = 'ETH'

balance, locked = client.get_asset_balance(asset=asset)

print(f" - Balance for {asset} = {balance} / locked = {locked}")

info = client.get_symbol_info('ETHUSDT')
print(info)

info = client.get_symbol_info('BTCUSDT')
print(info)

info = client.get_symbol_info('BNBUSDT')
print(info)


