import datetime as dt
import backtrader as bt
from backtrader_bybit import BybitStore
from ConfigBybit.Config import Config  # Configuration file


# Trading System
class JustPrintOHLCVStrategy(bt.Strategy):
    """
    Live strategy demonstration with SMA, RSI indicators
    """
    params = (  # Parameters of the trading system
        ('coin_target', ''),
        ('timeframe', ''),
    )

    def __init__(self):
        """Initialization, adding indicators for each ticker"""
        pass

    def next(self):
        """Arrival of a new ticker candle"""
        for data in self.datas:  # Running through all the requested bars of all tickers
            ticker = data._name
            status = data._state  # 0 - Live data, 1 - History data, 2 - None
            _interval = self.p.timeframe

            if status in [0, 1]:
                if status: _state = "False - History data"
                else: _state = "True - Live data"

                print('{} / {} [{}] - Open: {}, High: {}, Low: {}, Close: {}, Volume: {} - Live: {}'.format(
                    bt.num2date(data.datetime[0]),
                    data._name,
                    _interval,  # ticker timeframe
                    data.open[0],
                    data.high[0],
                    data.low[0],
                    data.close[0],
                    data.volume[0],
                    _state,
                ))


    def log(self, txt, dt=None):
        """Print string with date to the console"""
        dt = bt.num2date(self.datas[0].datetime[0]) if not dt else dt  # date or date of the current bar
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Print the date and time with the specified text to the console


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(200000)  # Setting how much money
    cerebro.broker.setcommission(commission=0.0015)  # Set the commission - 0.15% ... divide by 100 to remove %

    coin_target = 'USDT'  # the base ticker in which calculations will be performed
    symbol = 'BTC' + coin_target  # the ticker by which we will receive data in the format <CodeTickerBaseTicker>
    symbol2 = 'ETH' + coin_target  # the ticker by which we will receive data in the format <CodeTickerBaseTicker>

    accountType = Config.BYBIT_ACCOUNT_TYPE
    store = BybitStore(
        api_key=Config.BYBIT_API_KEY,
        api_secret=Config.BYBIT_API_SECRET,
        coin_target=coin_target,
        testnet=False,
        accountType=accountType,
    )  # Bybit Storage

    # # live connection to Bybit - for Offline comment these two lines
    # broker = store.getbroker()
    # cerebro.setbroker(broker)

    # -----------------------------------------------------------
    # Attention! - Now it's Offline for testing strategies      #
    # -----------------------------------------------------------

    # Historical 1-minute bars for 10 hours + new live bars / timeframe M1
    timeframe = "D1"
    from_date = dt.datetime.now() - dt.timedelta(days=4500)
    data = store.getdata(timeframe=bt.TimeFrame.Days, compression=1, dataname=symbol, start_date=from_date, LiveBars=True, rows_by_request=1000)  # set True here - if you need to get live bars
    data2 = store.getdata(timeframe=bt.TimeFrame.Days, compression=1, dataname=symbol2, start_date=from_date, LiveBars=True, rows_by_request=1000)  # set True here - if you need to get live bars

    cerebro.adddata(data)  # Adding data
    cerebro.adddata(data2)  # Adding data

    cerebro.addstrategy(JustPrintOHLCVStrategy, coin_target=coin_target, timeframe=timeframe)  # Adding a trading system

    cerebro.run()  # Launching a trading system
    # cerebro.plot()  # Draw a chart
