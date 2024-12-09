import datetime
import numpy as np
import backtrader as bt

from strategies.high_n_low_liquidity_pool.HnLLiquidity import HighAndLowLiquidity
from strategies.print_close import  MovingAverageCrossOver

capital = 100
data = bt.feeds.GenericCSVData(dataname='./data/XAUUSD--5--23.7.12--24.12.6.csv',
                               dtformat='%Y-%m-%d %H:%M',
                               fromdate=datetime.datetime(2023, 7, 13, 8),
                               todate=datetime.datetime(2023, 7, 15),
                               separator='\t', datetime=0, open=1, high=2,
                               low=3, close=4, openinterest=-1,
                               timeframe=bt.TimeFrame.Minutes,
                               preload=True,
                               )
cerebro = bt.Cerebro()
cerebro.broker.setcash(capital)
cerebro.adddata(data)
cerebro.optstrategy(HighAndLowLiquidity, atr_p=range(5, 20, 2),
                    risk_percentage=range(1, 5),
                    RR=range(1, 4),
                    compression=range(12, 54, 6),
                    SL_FACTOR=range(1, 4))

# Add analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days, riskfreerate=0.0)
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analysis')
cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

if __name__ == '__main__':
    optimized_runs = cerebro.run(optreturn=False)

    final_results_list = []
    for run in optimized_runs:
        for strat in run:
            sharpe_ratio = strat.analyzers.sharpe.get_analysis().get('sharperatio', 'N/A')
            max_drawdown = strat.analyzers.drawdown.get_analysis().max.drawdown
            trade_analysis = strat.analyzers.trade_analysis.get_analysis()
            sqn_stat = strat.analyzers.sqn.get_analysis()
            PnL = round(strat.broker.get_value() - capital, 2)
            final_results_list.append([strat.params.atr_p,
                                       strat.params.compression,
                                       strat.params.risk_percentage,
                                       strat.params.RR,
                                       strat.params.SL_FACTOR,
                                       PnL, max_drawdown,
                                       # round(trade_analysis.won.total / trade_analysis.total.closed * 100, 2),
                                       # trade_analysis.streak.won.longest,
                                       # trade_analysis.streak.lost.longest,
                                       sqn_stat.sqn])

    sorted_stats = sorted(final_results_list, key=lambda x: x[5], reverse=True)
    for line in sorted_stats[:5]:
        print(line)