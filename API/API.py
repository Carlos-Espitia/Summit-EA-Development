import math
import os
import MetaTrader5 as mt5
import json
from typing import List, TypedDict
from API.utils import Utils

# add option to draw on charts

DATA_FIlE = 'data.json'

# typings
class TakeProfitPartial(TypedDict):
    price: float
    lot: float

class SummitAPI:
    def __init__(self):
        self.trades = Trades()

    def initialize(self):
        # check if data json file exist
        if not os.path.exists(DATA_FIlE) or os.stat(DATA_FIlE).st_size == 0:
            data = {'trades': []}
            with open(DATA_FIlE, 'w') as file: json.dump(data, file, indent=4)

        if not mt5.initialize():
            print('Initialization failed, check internet connection. You must have Meta Trader 5 installed.')
            mt5.shutdown()
            quit()

        else:
            print(f'You are running the [name of algo] expert advisor,')


    # Symbol information 
    # might change to class to add types
    def getSymbolInfo(self, symbol: str): return mt5.symbol_info(symbol)
    def getSymbolInfoTick(self, symbol: str): return mt5.symbol_info_tick(symbol)
    def getPipsBetween(self, price1: float, price2: float, pipSize: float): return math.floor(((abs(price1 - price2) / pipSize) / 10.) *10) / 10 # check if math is correct later


class Trades:
    # Order type
    def __init__(self):
        self.ORDER_TYPE_BUY            = mt5.ORDER_TYPE_BUY            # Market Buy order
        self.ORDER_TYPE_SELL           = mt5.ORDER_TYPE_SELL           # Market Sell order
        self.ORDER_TYPE_BUY_LIMIT      = mt5.ORDER_TYPE_BUY_LIMIT      # Buy Limit pending order   | 2
        self.ORDER_TYPE_SELL_LIMIT     = mt5.ORDER_TYPE_SELL_LIMIT     # Sell Limit pending order  | 3

        self.tradePending = 1
        self.tradeActive = 0


    def execute(self, symbol: str, orderType: int, lot: float, comment="", priceEntry: float=None, trailStopLoss: float=None, stopLoss: float=None, takeProfit: float=None, takeProfitPartials: List[TakeProfitPartial]=None):
        
        valid_types = {self.ORDER_TYPE_BUY, self.ORDER_TYPE_SELL, self.ORDER_TYPE_BUY_LIMIT, self.ORDER_TYPE_SELL_LIMIT}
        if orderType not in valid_types:
            raise ValueError(f'Not valid order type')

        if orderType == self.ORDER_TYPE_BUY_LIMIT or orderType == self.ORDER_TYPE_SELL_LIMIT:
            if priceEntry == None: raise ValueError(f'Must include price entry for limit orders!')

        if orderType == self.ORDER_TYPE_BUY or orderType == self.ORDER_TYPE_SELL:
            if priceEntry: print(f'Auto changed price entry since it is market order') # fix none auto change thing later
        
        if orderType == self.ORDER_TYPE_BUY: 
            action = mt5.TRADE_ACTION_DEAL
            priceEntry = mt5.symbol_info_tick(symbol).ask

        if orderType == self.ORDER_TYPE_SELL: 
            action = mt5.TRADE_ACTION_DEAL
            priceEntry = mt5.symbol_info_tick(symbol).bid

        if orderType == self.ORDER_TYPE_BUY_LIMIT: action = mt5.TRADE_ACTION_PENDING
        if orderType == self.ORDER_TYPE_SELL_LIMIT: action = mt5.TRADE_ACTION_PENDING

            
        request = {
            "action": action,
            "symbol": symbol,
            "volume": lot, # Amount of lots you want to buy 
            "type": orderType, # buy or sell | price ask and bid must match
            "price": priceEntry, # put ask or bid price | depends if wanna short or long | other prices arent valid except those 2
            "deviation": 10, # max threshold of slippage allowed when trade executed
            "magic": 0, # idk
            "comment": comment, # we could use this for iding order/positions or adding extra features like trailing stoploss
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        print(request)

        if trailStopLoss and stopLoss: raise ValueError(f'You can not use trail stop and a stoploss at the same time')


        if stopLoss: request["sl"] = stopLoss
        if takeProfit: request["tp"] = takeProfit

        # TODO:
        # for limit order you must have to wait putting in partials, partials will execute if tapped or already above or below actual trade 
        # limit orders cant be used as partials, we will have to constantly loop to check if partials were hit

        if takeProfitPartials:

            # Validate lot and price partials
            entry_price = request["price"]
            total_lot = request["volume"]
            order_type = request["type"]

            partial_lot_sum = 0
            for partial in takeProfitPartials:
                partial_price = partial["price"]
                partial_lot = partial["lot"]

                # Sum up the lots
                partial_lot_sum += partial_lot

                # Check if the partial lot exceeds total lot size
                if partial_lot_sum >= total_lot:
                    raise Utils.error("Partial lot size exceed or equal to total lot size.")
                
                # Validate take profit based on order type
                if order_type == (self.ORDER_TYPE_SELL or self.ORDER_TYPE_SELL_LIMIT) and partial_price >= entry_price:
                    raise Utils.error(F"For a SELL order, partials must be below the entry price.\n {partial_price} | {entry_price} | {order_type}")

                elif order_type == (self.ORDER_TYPE_BUY or self.ORDER_TYPE_BUY_LIMIT) and partial_price <= entry_price:
                    raise Utils.error("For a BUY order, partials must be above the entry price.")

                # If all checks pass for this partial, it's valid
                # print(f"Partial take profit at {partial_price} with lot {partial_lot} is valid.")

                
        result = mt5.order_send(request)

        if result == None: return result
        if result.retcode != mt5.TRADE_RETCODE_DONE: print("Order send failed with error code:", result.retcode)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print("Order send successful with order ID:", result.order)

            # extra data should be added to json
            tradeData = {
                'id': result.order, # id here | figure out how to get trade id 
            }

            if takeProfitPartials: 

                # orderType2 = None

                # weird had to add () to conditions
                # if result.request.type == (self.ORDER_TYPE_BUY or self.ORDER_TYPE_BUY_LIMIT): orderType2 = self.ORDER_TYPE_SELL_LIMIT
                # if result.request.type == (self.ORDER_TYPE_SELL or self.ORDER_TYPE_SELL_LIMIT): orderType2 = self.ORDER_TYPE_BUY_LIMIT

                # successfulPartialOrders = []

                for partial in takeProfitPartials:
                    print(f"{partial}")

                    # partialPrice = partial["price"]

                    # put lines on the chart

                    # use a mql5 file to draw lines on chart by using network communication

                    # partialOrder = self.execute(
                    #     symbol=symbol,
                    #     orderType=orderType2,
                    #     priceEntry=partials["price"],
                    #     lot=partials["lot"]
                    # )

                    # if partialOrder == None:
                    #     self.close(result.order)
                    #     for partialOrderId in successfulPartialOrders:
                    #         self.close(partialOrderId)
                    #     raise Utils.error("There was an error in putting partials")
                    
                    # else: 
                    #     successfulPartialOrders.append(partialOrder.order)
                
                tradeData["takePartials"] = takeProfitPartials

            with open(DATA_FIlE, 'r') as file:
                data = json.load(file)

            # Update the data
            # this will include partials too
            data['trades'].append(tradeData)

            with open(DATA_FIlE, 'w') as file:
                json.dump(data, file)

        return result
    


    # TODO:
    # order limits | tp, sl, price entry | can't modify lotsize of pending order 
    # active orders | tp, sl | Still need to test 

    # set 0.0 to sl and tp to remove
    def modify(self, id: int, stopLoss: float=None, takeProfit: float=None, entryPrice: float=None):
        tradeData, type = self.getTradeData(id)

        print(tradeData)

        if type == 'order':
            request = {
                "order": id,
                "action": mt5.TRADE_ACTION_MODIFY,
                "symbol": tradeData.symbol,
                # "volume": tradeData.volume_current,
                "price": tradeData.price_open,
                "tp": tradeData.tp,
                "sl": tradeData.sl
            }

            # if lotSize != None: request["volume"] = lotSize
            if entryPrice: request["price"] = entryPrice
            if takeProfit: request["tp"] = takeProfit
            if stopLoss: request["sl"] = stopLoss

        if type == 'position':
            request = {
                "position": id,
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": tradeData.symbol,
                "tp": tradeData.tp,
                "sl": tradeData.sl
            }

            if takeProfit: request["tp"] = takeProfit
            if stopLoss: request["sl"] = stopLoss



        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE: print("Modifying trade failed with error code:", result.retcode)
        if result.retcode == mt5.TRADE_RETCODE_DONE: print("Modifying trade successeeded with code:", result.retcode)
        
        return result
    

    def close(self, id: int): 
        tradeData, type = self.getTradeData(id)

        request = None

        # print(type)

        if type == 'order':
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": id,
                "comment": "Order Removed"
            }

        if type == 'position': 
            tick = mt5.symbol_info_tick(tradeData.symbol)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": id,
                "symbol": tradeData.symbol,
                "volume": tradeData.volume,
                "type": mt5.ORDER_TYPE_BUY if tradeData.type == 1 else mt5.ORDER_TYPE_SELL, # if position type was a buy switch to sell to close trade, same with opposite way 
                "price": tick.ask if tradeData.type == 1 else tick.bid,  
                # "deviation": 20,
                # "magic": 100,
                "comment": "close position",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE: print("Closing trade failed with error code:", result.retcode)
        if result.retcode == mt5.TRADE_RETCODE_DONE: print("Closing trade succeeded with code:", result.retcode)
        return result

    # return object
    # pip wons/loss
    # tp
    # sl
    # etc...
    # might add extra data here 
    def getTradeData(self, id: int): 
        if not self.checkTradeExist(id): raise ValueError(f'Trade does not exist!')
        if mt5.positions_get(ticket=id): return [mt5.positions_get(ticket=id)[0], 'position']
        if mt5.orders_get(ticket=id): return [mt5.orders_get(ticket=id)[0], 'order']

    def checkTradeExist(self, id: int): 
        if mt5.positions_get(ticket=id): return True
        if mt5.orders_get(ticket=id): return True
        return False 
    
    
#######################################################
#interval #############################################
#######################################################


# have to check if id changes

def checkLimitOrderExecution():
    orders = mt5.orders_get()
    print(orders)

# Utils.setInterval(checkLimitOrderExecution, 1000)