from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma


def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        # We want a 15 period SMA over the closing prices.
        self.__sma15 = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__sma50 = ma.SMA(feed[instrument].getCloseDataSeries(), 50)
        self.__sma200 = ma.SMA(feed[instrument].getCloseDataSeries(), 200)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        # self.info("%s, %s, %s, %s" % (bar.getClose()
        print("%s, %s, %s, %s, %s" % (
            bar.getDateTime()
            , bar.getClose()
            , safe_round(self.__sma15[-1], 2)
            , safe_round(self.__sma50[-1], 2)
            , safe_round(self.__sma200[-1], 2))
        )


# Load the bar feed from the CSV file
feed = quandlfeed.Feed()
# feed.addBarsFromCSV("orcl", "WIKI-ORCL-2000-quandl.csv")
feed.addBarsFromCSV("orcl", "ORCL.csv")

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, "orcl")
myStrategy.run()
