import backtrader as bt
import sys
import inspect

class PrintClose(bt.Strategy):
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] data series
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        print(f'{dt.strftime('%Y-%m-%d %H:%M')} {txt}')
    def next(self):
        self.log(f'Close: {self.dataclose[0]}')


class MovingAverageCrossOver(bt.Strategy):
    params = (('pfast', 20), ('pslow', 50))

    def __init__(self):
        self.caller_script = sys.argv[0].split('\\')[-1]
        self.order = None
        self.dataclose = self.datas[0].close
        # Instantiate moving averages
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.pslow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.pfast)
        self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)

    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            # We have an ongoing order, or we have submitted order already, do nothing
            return

        if order.status in [bt.Order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            # for whatever reason the order was not filled
            self.log('Order Canceled/Margin/Rejected')

        # reset order
        self.order = None

    def next(self):
        if self.order:
            # if we have an open order, do nothing
            return

        if not self.position: # if we are not in the market look for signals
            if self.crossover > 0: # fast sma crosses above slow sma: BUY
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()

            elif self.crossover < 0: # fast sma crosses below slow sma: SELL
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        if self.caller_script == 'main.py':
            print(f'{dt.strftime('%Y-%m-%d %H:%M')} {txt}')