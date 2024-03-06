import backtrader as bt
from backtrader_bybit import BybitStore
from ConfigBybit.Config import Config
from decimal import Decimal

cerebro = bt.Cerebro(quicknotify=True)

cerebro.broker.setcash(100000)  # Устанавливаем, сколько денег
cerebro.broker.setcommission(commission=0.0015)  # Установленная комиссия - 0,15%... разделите на 100, чтобы удалить %

coin_target = 'USDT'  # базовый тикер, в котором будут выполняться вычисления
symbols = ('BTC', 'ETH', 'BNB')  # тикеры, по которым мы будем получать данные

accountType = Config.BYBIT_ACCOUNT_TYPE
store = BybitStore(
    api_key=Config.BYBIT_API_KEY,
    api_secret=Config.BYBIT_API_SECRET,
    coin_target=coin_target,
    testnet=False,
    accountType=accountType,
)  # Bybit Storage

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

