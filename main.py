import datetime
import backtrader as bt
from strategies.high_n_low_liquidity_pool.HnLLiquidity import HighAndLowLiquidity

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DD')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='RETURNS')
    cerebro.broker.setcommission(mult=100)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days, riskfreerate=0.0)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analysis')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

    data = bt.feeds.GenericCSVData(dataname='./data/XAUUSD--5--23.7.12--24.12.6.csv',
                                   dtformat='%Y-%m-%d %H:%M',
                                   fromdate=datetime.datetime(2023, 7, 13, 8),
                                   todate=datetime.datetime(2024, 12, 6,),
                                   separator='\t', datetime=0, open=1, high=2, low=3,
                                   close=4, openinterest=-1, timeframe=bt.TimeFrame.Minutes, compression=5
                                   )

    cerebro.adddata(data)
    cerebro.addstrategy(HighAndLowLiquidity, atr_p=5, risk_percentage=3, RR=1, SL_FACTOR=1, compression=30)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()

    # Access the first strategy's analyzers
    strat = results[0]

    # Sharpe Ratio
    sharpe_ratio = strat.analyzers.sharpe.get_analysis().get('sharperatio', 'N/A')
    print(f"Sharpe Ratio: {sharpe_ratio}")

    # Drawdown
    drawdown = strat.analyzers.drawdown.get_analysis()
    print(f"Max Drawdown: {drawdown.max.drawdown:.2f}%")
    print(f"Money Lost During Max Drawdown: {drawdown.max.moneydown:.2f}")

    # Trade Analysis
    trade_analysis = strat.analyzers.trade_analysis.get_analysis()
    print(f"Total Trades: {trade_analysis.total.closed}")
    print(f"Win Rate: {trade_analysis.won.total / trade_analysis.total.closed * 100:.2f}%")
    print(f"Consecutive Wins: {trade_analysis.streak.won.longest}")
    print(f"Consecutive Losses: {trade_analysis.streak.lost.longest}")
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    sqn_stat = strat.analyzers.sqn.get_analysis()
    print(f"SQN: {sqn_stat.sqn}")
    print(f"SQN Trade No: {sqn_stat.trades}")

