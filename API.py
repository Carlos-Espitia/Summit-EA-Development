import MetaTrader5 as mt5
from datetime import datetime, timedelta
import json

class SummitAPI:

    def initialize():
        if not mt5.initialize():
            print('Initialization failed, check internet connection. You must have Meta Trader 5 installed.')
            mt5.shutdown()
            quit()

        else:
            print(f'You are running the [name of algo] expert advisor,')

    # Symbol information
    # might change to class to add types
    def getSymbolInfo(symbol: str): return mt5.symbol_info(symbol)
    def getSymbolInfoTick(symbol: str): return mt5.symbol_info_tick(symbol)

    

    class trades:
        ORDER_TYPE_BUY                      = 0      # Market Buy order
        ORDER_TYPE_SELL                     = 1      # Market Sell order
        ORDER_TYPE_BUY_LIMIT                = 2      # Buy Limit pending order
        ORDER_TYPE_SELL_LIMIT               = 3      # Sell Limit pending order

        def execute(symbol: str, orderType: int, lot: float, id: int, comment="", priceEntry: float=None, stopLoss: float=None, takeProfit: float=None, duration: int=None):
            
            valid_types = {0, 1, 2, 3}
            if orderType not in valid_types:
                raise ValueError(f'Not valid order type')
            
            print(priceEntry)
            if orderType == 2 or orderType == 3 and priceEntry is None: raise ValueError(f'Must include price entry for limit orders!')
            #fix none thing
            if orderType == 0 or orderType == 1 and priceEntry is not None: print(f'Auto changed price entry since it is market order')
            if orderType == 0: priceEntry = mt5.symbol_info_tick(symbol).ask
            if orderType == 1: priceEntry = mt5.symbol_info_tick(symbol).bid
                
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot, # Amount of lots you want to buy 
                "type": orderType, # buy or sell | price ask and bid must match
                "price": priceEntry, # put ask or bid price | depends if wanna short or long | other prices arent valid except those 2
                "deviation": 10, # max threshold of slippage allowed when trade executed
                "magic": id, # used for identifying trade by developer
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }

            # updates tp & sl data
            if stopLoss is not None: request["sl"] = stopLoss
            if takeProfit is not None: request["tp"] = takeProfit
        

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE: print("Order send failed with error code:", result.retcode)
            if result.retcode == mt5.TRADE_RETCODE_DONE: print("Order send successful with order ID:", result.order)

            return result
            

# # example 1
# SummitAPI.trades.execute(
#     symbol="EURUSD",
#     orderType=SummitAPI.trades.ORDER_TYPE_BUY,
#     lot=1.5,
#     id=0,
#     sl=1.000,
#     tp=1.100,
#     duration=10000
# )

# # example 2
# SummitAPI.trades.execute(
#     symbol="EURUSD",
#     orderType=SummitAPI.trades.ORDER_TYPE_BUY_LIMIT,
#     priceEntry=1.500,
#     lot=1.5,
#     id=0,
#     sl=1.000,
#     tp=1.100,
#     duration=10000
# )


# SummitAPI.execute_trade(
#     symbol=ticker,
#     type="BUY", # BUY | SELL | BUY LIMIT | SELL LIMIT
#     lot=1,
#     sl="price",
#     tp="price",
#     id=1,
#     duration=100, # duration of canceling order | might change to date
#     )


# request = {
#     "action": mt5.TRADE_ACTION_DEAL,
#     "symbol": ticker,
#     "volume": lot, # Amount of lots you want to buy 
#     "type": mt5.ORDER_TYPE_BUY, # buy or sell | price ask and bid must match
#     "price": price, # put ask or bid price | depends if wanna short or long | other prices arent valid except those 2
#     "sl": price - 100 * point,
#     "tp": price + 100 * point,
#     "deviation": 20, # max threshold of slippage allowed when trade executed
#     "magic": 1, # used for identifying trade by developer
#     "comment": "Testing this trade",
#     "type_time": mt5.ORDER_TIME_GTC,
#     "type_filling": mt5.ORDER_FILLING_FOK,
# }