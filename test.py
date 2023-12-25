# Copyright 2023, Carlos Espitia
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
from API.API import SummitAPI
from API.socket import Server
from typing import List, TypedDict


# Connect to the MetaTrader 5 terminal
summitAPI = SummitAPI()
summitAPI.initialize()

current_price = summitAPI.getSymbolInfoTick("EURUSD").bid
targets = 0.00050

# summitAPI.getSymbolInfo("EURUSD").
# Notes
# Figure out how to add a setintverval for constantly checking trades for trailstops
# Add trail stoploss
# Add tp partials

# socket.gethostbyname(socket.gethostname()) # get my hostname and use that to get host ip
server = Server()
server.start()



# market order
# result = summitAPI.trades.execute(
#     symbol="EURUSD",
#     orderType=summitAPI.trades.ORDER_TYPE_SELL,
#     lot=0.3, # doesnt allow whole numbers for some weird reason
#     takeProfitPartials=[{ 'price': 1.09150, 'lot': 0.1}, { 'price': 1.09100, 'lot': 0.1}] # add checks for it take partials are under or above
#     # takeProfit=current_price + targets,
#     # stopLoss=current_price - targets
# )

# print(result)
# limit order

# result = summitAPI.trades.execute(
#     symbol="EURUSD",
#     orderType=summitAPI.trades.ORDER_TYPE_BUY_LIMIT,
#     priceEntry=1.09400,
#     lot=0.3,
#     takeProfitPartials=[{ 'price': 1.09600, 'lot': 0.1}, { 'price': 1.09550, 'lot': 0.1}], # add checks for it take partials are under or above
#     takeProfit=1.09650,
#     stopLoss=1.09300
# )

# print(mt5.orders_get())

# modify trades
# result = summitAPI.trades.modify(
#     id=1699877856, 
#     entryPrice=1.09900, 
#     takeProfit=1.1,
#     stopLoss=1.09700
# )

# close orders and positions
# summitAPI.trades.close(id=1734716670)


# print(result)



# mt5.shutdown() # this the MT5 initialization
