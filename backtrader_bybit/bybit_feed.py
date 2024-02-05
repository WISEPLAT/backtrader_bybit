from collections import deque
from datetime import datetime, timezone, timedelta, time, date
from time import sleep


from backtrader.feed import DataBase
from backtrader.utils import date2num

from backtrader import TimeFrame as tf


class BybitData(DataBase):
    """Class for getting historical and live ticker data"""
    params = (
        ('drop_newest', False),
    )
    
    # States for the Finite State Machine in _load
    _ST_LIVE, _ST_HISTORBACK, _ST_OVER = range(3)

    def __init__(self, store, **kwargs):  # def __init__(self, store, timeframe, compression, start_date, LiveBars):
        """Initialization of required variables"""
        self.timeframe = tf.Minutes
        self.compression = 1
        self.start_date = None
        self.LiveBars = None

        self._state = None

        self.symbol = self.p.dataname

        if hasattr(self.p, 'timeframe'): self.timeframe = self.p.timeframe
        if hasattr(self.p, 'compression'): self.compression = self.p.compression
        if 'start_date' in kwargs: self.start_date = kwargs['start_date']
        if 'LiveBars' in kwargs: self.LiveBars = kwargs['LiveBars']

        self._store = store
        self._data = deque()

        self.all_history_data = None  # all history by ticker
        self.all_ohlc_data = []  # all history by ticker
        # print("Ok", self.timeframe, self.compression, self.start_date, self._store, self.LiveBars, self.symbol)

    def _load(self):
        """Download method"""
        if self._state == self._ST_OVER:
            return False
        elif self._state == self._ST_LIVE:
            # return self._load_kline()
            if self._load_kline():
                return True
            else:
                self._start_live()
        elif self._state == self._ST_HISTORBACK:
            if self._load_kline():
                return True
            else:
                self._start_live()

    def _load_kline(self):
        """Processing a single row of data"""
        try:
            kline = self._data.popleft()
        except IndexError:
            return None

        if type(kline) == list:
            timestamp, open_, high, low, close, volume, turnover = kline
            self.lines.datetime[0] = date2num(datetime.fromtimestamp(int(timestamp) / 1000))
            self.lines.open[0] = float(open_)
            self.lines.high[0] = float(high)
            self.lines.low[0] = float(low)
            self.lines.close[0] = float(close)
            self.lines.volume[0] = float(volume)

        return True

    def _start_live(self):
        """Getting live data"""
        buf_klines_last_sec = {}
        while True:
            if self.LiveBars:

                if self._state != self._ST_LIVE:
                    print(f"Live started for ticker: {self.symbol}")
                    self._state = self._ST_LIVE
                    self.put_notification(self.LIVE)

                if not self.get_live_bars_from:
                    self.get_live_bars_from = datetime.now()

                _now = datetime.now() + timedelta(minutes=1)
                klines = self._store.bybit_session.get_kline(
                    category=self._store.category,
                    symbol=self.symbol,
                    interval=self.interval,
                    start=round(self.get_live_bars_from.timestamp()*1000),  # in milliseconds
                    end=round(_now.timestamp()*1000),  # in milliseconds
                )

                # if there is something to process
                if 'result' in klines and 'list' in klines['result'] and klines['result']['list']:
                    new_klines = klines['result']['list']  # taking new rows of data
                    _empty = True
                    _klines = []

                    _previous_candle_time, _current_candle_time, _future_candle_time = self.get_previous_future_candle_time()
                    # print(_previous_candle_time, _current_candle_time, _future_candle_time)

                    # ----------
                    # 2024-02-04 16:35:00 | 2024-02-04 16:35:00 2024-02-04 16:36:00 2024-02-04 16:37:00 | 2024-02-04 16:36:00.136035
                    # ----------
                    # 2024-02-04 16:35:00 / BTCUSDT [1] - Open: 43008.49, High: 43012.36, Low: 42980.45, Close: 42980.45, Volume: 5.085419 - Live: True - Live data
                    # ----------
                    # 2024-02-04 16:35:00 | 2024-02-04 16:35:00 2024-02-04 16:36:00 2024-02-04 16:37:00 | 2024-02-04 16:36:00.339052
                    # 2024-02-04 16:34:00 | 2024-02-04 16:35:00 2024-02-04 16:36:00 2024-02-04 16:37:00 | 2024-02-04 16:36:00.339052
                    # ----------
                    # ----------
                    # 2024-02-04 16:35:00 | 2024-02-04 16:35:00 2024-02-04 16:36:00 2024-02-04 16:37:00 | 2024-02-04 16:36:00.542093
                    # ----------
                    # 2024-02-04 16:35:00 / BTCUSDT [1] - Open: 43008.49, High: 43012.36, Low: 42980.31, Close: 42980.31, Volume: 5.08668 - Live: True - Live data
                    # ----------
                    # 2024-02-04 16:35:00 | 2024-02-04 16:35:00 2024-02-04 16:36:00 2024-02-04 16:37:00 | 2024-02-04 16:36:00.742522
                    # ----------

                    # To prevent situation, when in last second we can get two candles - let's add to _previous_candle_time +1..3 seconds

                    # print("----------")
                    for kline in new_klines:
                        dt = datetime.fromtimestamp(int(kline[0]) / 1000)
                        if dt <= _previous_candle_time:
                            # print(dt, "|", _previous_candle_time, _current_candle_time, _future_candle_time, "|", datetime.now())
                            buf_klines_last_sec[dt] = kline  # can be several for one time
                            # if kline not in self.all_history_data:  # if there is no such data row,
                            #     self.all_history_data.append(kline)
                            #     _klines.append(kline)
                            #     _empty = False
                    # print("----------")

                    # print(len(buf_klines_last_sec), _current_candle_time + timedelta(seconds=1) < datetime.now() < _current_candle_time + timedelta(seconds=3))
                    # print(dt, "|", _previous_candle_time, _current_candle_time, _future_candle_time, "|", datetime.now())
                    if len(buf_klines_last_sec) and _current_candle_time + timedelta(seconds=1) < datetime.now() < _current_candle_time + timedelta(seconds=3):
                        for dt, kline in buf_klines_last_sec.items():
                            if kline not in self.all_history_data:  # if there is no such data row,
                                # print(dt, "|", _previous_candle_time, _current_candle_time, _future_candle_time, "|", datetime.now())
                                self.all_history_data.append(kline)
                                _klines.append(kline)
                                _empty = False
                                self.get_live_bars_from = dt
                        buf_klines_last_sec = {}

                    self._data.extend(_klines)  # we are sending it for processing
                    if _klines or _empty:  # if you have received new data
                        break

                # here you can optimize through threads and request less often, recalculating how long to wait
                sleep(1)

            else:
                self._state = self._ST_OVER
                break

    def haslivedata(self):
        return self._state == self._ST_LIVE and self._data

    def islive(self):
        return True

    def start(self):
        """Getting historical data"""
        DataBase.start(self)

        # if the TF is not set correctly, then we do nothing
        self.interval = self._store.get_interval(self.timeframe, self.compression)
        if self.interval is None:
            self._state = self._ST_OVER
            self.put_notification(self.NOTSUPPORTED_TF)
            return

        # if we can't get the ticker data, then we don't do anything
        self.symbol_info = self._store.get_symbol_info(self.symbol)
        if self.symbol_info is None:
            self._state = self._ST_OVER
            self.put_notification(self.NOTSUBSCRIBED)
            return

        # getting historical data
        if self.start_date:
            self._state = self._ST_HISTORBACK
            self.put_notification(self.DELAYED)

            _now = datetime.now()
            klines = self._store.bybit_session.get_kline(
                category=self._store.category,
                symbol=self.symbol,
                interval=self.interval,
                start=round(self.start_date.timestamp()*1000),  # in milliseconds
                end=round(_now.timestamp()*1000),  # in milliseconds
            )

            self.get_live_bars_from = _now

            print(f"- {self.symbol} - History data - Ok")

            if 'result' in klines and 'list' in klines['result'] and klines['result']['list']:
                klines = klines['result']['list']
                klines = klines[::-1]  # inverse
                klines = klines[:-1]  # -1 last row as it can be in process of forming
            else:
                klines = []

            self.all_history_data = klines  # first receive of the history -> save it to a list

            try:
                if self.p.drop_newest:
                    klines.pop()
                self._data.extend(klines)
            except Exception as e:
                print("Exception (try set from_date in utc format):", e)

        else:
            self._start_live()

    def get_previous_future_candle_time(self, ):
        # timeframe = "D1"
        now = datetime.now()
        # now = datetime.datetime.fromisoformat("2023-03-20 00:00")
        now_hour = now.hour
        now_minutes = now.minute

        _previous_candle_time, _current_candle_time, _future_candle_time = None, None, None

        if self.interval in ["D", "W", "M"]:
            _current_candle_time = datetime.fromisoformat(now.strftime('%Y-%m-%d') + " " + "00:00")
            # print(_current_candle_time)

            days_back = 1  # for D
            if self.interval == "W":  # for week
                day_of_week = _current_candle_time.weekday()  # number of day in week
                days_back = day_of_week + 1
            if self.interval == "M":  # for month
                num_days = (datetime.now().date() - date(now.year, now.month, 1)).days
                days_back = num_days + 1

            _previous_candle_time = _current_candle_time - timedelta(days=days_back)
            _future_candle_time = _current_candle_time + timedelta(days=days_back)
            # print(_previous_candle_time)
            # print(_future_candle_time)

        if self.interval in ['1', '3', '5', '15', '30', '60', '120', '240', '360', '720']:
            _minutes = int(self.interval)

            # H1 .. M1
            now_minutes = (now_minutes // _minutes) * _minutes
            pre_minutes = (now_minutes // _minutes + 1) * _minutes - now_minutes

            _current_candle_time = datetime.fromisoformat(
                now.strftime('%Y-%m-%d') + " " + f"{now_hour:02}:{now_minutes:02}")
            # print(_current_candle_time)

            _previous_candle_time = _current_candle_time - timedelta(minutes=pre_minutes)
            _future_candle_time = _current_candle_time + timedelta(minutes=pre_minutes)
            # print(_previous_candle_time)
            # print(_future_candle_time)

        return _previous_candle_time, _current_candle_time, _future_candle_time
