import backtrader as bt
from datetime import timedelta


UTC_PLUS_ONE = timedelta(hours=1)


# Create a custom data feed to adjust the time
class MyDataFeed(bt.feeds.GenericCSVData):
    def _load(self):
        result = super()._load()

        # Get the current datetime (the value is in float format)
        if self.datetime.datetime() is not None:
            # Convert float to datetime object
            dt = self.data.datetime[0]
            date_time = bt.num2date(dt)

            # Adjust the time by adding UTC+1 (1 hour)
            adjusted_time = date_time + UTC_PLUS_ONE

            # Convert the adjusted time back to the Backtrader format (float)
            self.data.datetime[0] = bt.date2num(adjusted_time)

        return result