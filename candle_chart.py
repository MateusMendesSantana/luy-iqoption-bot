import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates, ticker
import matplotlib as mpl
from mpl_finance import candlestick_ohlc
from datetime import datetime
from candle import Candle

class CandleChart:

    def __init__(self, active_code: str, time_interval: int):
        self.active_code = active_code
        self.time_interval = time_interval

        mpl.style.use('default')

    def setCandles(self, candles: list):
        ohlc_data = []

        for candle in candles:
            candle: Candle = candle
            ts = datetime.fromtimestamp(candle._from).strftime('%Y-%m-%d %H:%M:%S')

            ohlc_data.append(
                (dates.datestr2num(ts),
                np.float64(candle.open),
                np.float64(candle.max),
                np.float64(candle.min),
                np.float64(candle.close))
            )

        fig, ax1 = plt.subplots()
        candlestick_ohlc(
            ax1,
            ohlc_data,
            width = 1 / (24 * 60 * self.time_interval),
            colorup = 'g',
            colordown = 'r',
            alpha = 0.8)

        ax1.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))

        plt.xticks(rotation = 30)
        plt.grid()
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Historical Data ' + self.active_code)
        plt.tight_layout()
        plt.show()
        print('')
