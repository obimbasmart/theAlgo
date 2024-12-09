import datetime
import backtrader as bt
import pytz


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Define the timezone for Nigeria (WAT - West Africa Time, GMT+1)
    nigeria_tz = pytz.timezone('Africa/Lagos')

    data = bt.feeds.GenericCSVData(dataname='./data/XAUUSD--5--23.7.12--24.12.6.csv',
                                   dtformat='%Y-%m-%d %H:%M',
                                   fromdate=datetime.datetime(2024, 12, 6, 8),
                                   todate=datetime.datetime(2024, 12, 6, 18),
                                   separator='\t', datetime=0, open=1, high=2, low=3, close=4,
                                   openinterest=-1, timeframe=bt.TimeFrame.Minutes, compression=5,
                                   timezone=nigeria_tz
                                   )

    cerebro.adddata(data)
    result = cerebro.run()
    cerebro.plot(style='candlestick', stdstats=False)