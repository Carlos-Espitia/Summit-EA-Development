# Copyright 2023, Carlos Espitia
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
from API import SummitAPI


# Connect to the MetaTrader 5 terminal
SummitAPI.initialize()

# info
ticker = "EURUSD"
pipValue = SummitAPI.getSymbolInfo(ticker).point # Gets pip value 
price =  SummitAPI.getSymbolInfoTick(ticker).ask # Gets ask price to execute trade | non valid ask/bid prices entered will cancel the order


# execute trade
result = SummitAPI.trades.execute(
    symbol=ticker,
    orderType=SummitAPI.trades.ORDER_TYPE_BUY,
    lot=1.5,
    id=0,
    takeProfit=price + 100 * pipValue,
    stopLoss=price - 100 * pipValue,
    duration=10000
)

print(result)


mt5.shutdown()
