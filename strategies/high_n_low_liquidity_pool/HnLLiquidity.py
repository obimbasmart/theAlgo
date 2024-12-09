import backtrader as bt
import sys
import inspect

class HighAndLowLiquidity(bt.Strategy):
    params = (('atr_p', 14), ('risk_percentage', 1),
              ('RR', 2), ('SL_FACTOR', 1), ('compression', 12),)

    def __init__(self):
        self.caller_script = sys.argv[0].split('\\')[-1]
        self.p_high = None
        self.p_low = None
        self.order = None
        self.sl_order = None
        self.tp_order = None
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataclose = self.datas[0].close
        self.bar_executed = None
        self.atr = bt.indicators.ATR(self.datas[0], period=self.params.atr_p)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        if self.caller_script == 'main.py':
            print(f'{dt.strftime('%Y-%m-%d %H:%M')} {txt}')

    def next(self):
        if self.order:
            return

        if len(self) % self.params.compression == 0:
            self.p_high = max([self.datas[0].high[-i] for i in range(self.params.compression)])
            self.p_low = min([self.datas[0].low[-i] for i in range(self.params.compression)])

        if not self.position and self.p_high and self.p_low:
            if (self.datahigh[0] > self.p_high) and (self.dataclose[0] < self.p_high): # ::: BUY
                ENTRY = self.dataclose[0]
                SL = ENTRY + (self.atr[0])
                TP = ENTRY - (self.params.RR * self.atr[0])
                self.log(f' == SELL CREATE == \n\tEntry: {ENTRY:.2f}\n\tSL: {SL:.2f}\n\tTP: {TP:.2f}\n\tATR: {self.atr[0]:.4f}')
                self.order, self.sl_order, self.tp_order = self.sell_bracket(
                    size=(self.broker.get_value() * self.params.risk_percentage / 100) / (self.params.SL_FACTOR * self.atr[0] * 100),
                    price=None,  # market order
                    stopprice= SL,
                    limitprice = TP
                )

            elif (self.datalow[0] < self.p_low) and (self.dataclose[0] > self.p_low):
                ENTRY = self.dataclose[0]
                SL = ENTRY - (self.atr[0])
                TP = ENTRY + (self.params.RR * self.atr[0])
                self.log(f' == BUY CREATE == \n\tEntry: {self.dataclose[0]:.4f}\n\tSL: {SL:.4f}\n\tTP: {TP:.4f}\n\tATR: {self.atr[0]:.4f}')
                self.order, self.sl_order, self.tp_order = self.buy_bracket(
                    size= (self.broker.get_value() * self.params.risk_percentage / 100) / (self.atr[0] * self.params.SL_FACTOR * 100),
                    price=None,  # market order
                    stopprice=SL,
                    limitprice=TP,
                )


    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            # We have an ongoing order, or we have submitted order already, do nothing
            return

        if order.status in [bt.Order.Completed]:
            if order == self.order:
                if order.isbuy():
                    self.log(f'BUY EXECUTED, {order.executed.price:.4f}')
                elif order.issell():
                    self.log(f'SELL EXECUTED, {order.executed.price:.4f}')

            elif order == self.sl_order:
                self.log(f"Stop-loss hit at {order.executed.price}")
                self.order = None
            elif order == self.tp_order:
                self.log(f"Take-profit hit at {order.executed.price}")
                self.order = None

        elif order.status in [bt.Order.Margin, bt.Order.Rejected]:
            # for whatever reason the order was not filled
            self.log('Order Margin/Rejected')
            self.order = None