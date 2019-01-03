import datetime
import numpy as np

from myengine.backtest import Backtest
from myengine.data import HistoricCSVDataHandler
from myengine.event import SignalEvent
from myengine.execution import SimulatedExecutionHandler
from myengine.portfolio import Portfolio
from myengine.strategy import Strategy







if __name__ == "__main__":
    csv_dir = r"~/data"
    symbol_list = ['000001.SH','000001']
    initial_capital = 100000.0
    start_date = datetime.datetime(1990,1,1,0,0,0)
    heartbeat = 0.0
    
#default:    MACS = MovingAverageCrossStrategy(short_window=10,long_window=30)
    MACS = Strategy.MovingAverageCrossStrategy
    backtest = Backtest(csv_dir, 
                        symbol_list, 
                        initial_capital, 
                        heartbeat,
                        start_date,
                        HistoricCSVDataHandler, 
                        SimulatedExecutionHandler, 
                        Portfolio, 
                        MACS)

    backtest.simulate_trading()
