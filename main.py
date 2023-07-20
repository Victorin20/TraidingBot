import MetaTrader5 as mt5

mt5.initialize()

# Select the desired symbol
symbol = "EURUSD"
one_sell = False
one_buy = False


# Request the last tick for the symbol
last_tick = mt5.symbol_info_tick(symbol)
ticket_numbers = []
# Get the list of positions on symbols whose names contain "*USD*"
usd_positions = mt5.positions_get(group="*USD*")
if usd_positions is None:
    print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
elif len(usd_positions) > 0:
    # Extract the ticket numbers from the positions list
    ticket_numbers = [position.ticket for position in usd_positions]

for k in range(len(ticket_numbers)):
        ticket_to_find = ticket_numbers[k]
        comment = None
        for position in usd_positions:
            if position.ticket == ticket_to_find:
                comment = position.comment
                if comment == "sell":
                    one_sell = True
                if comment == "buy":
                    one_buy = True


def sell_order(volume):

    # Set the order type
    order_type = mt5.ORDER_TYPE_SELL


    # Set the stop loss and take profit levels (optional)
    stop_loss = 250.0  # Stop loss level in points
    take_profit = 250.0  # Take profit level in points

    # Set the order price (optional, if not market order)
    price = mt5.symbol_info_tick(symbol).bid
    sl = 1.0  # Optional: Set the stop loss level (in points)
    tp = 2.0  # Optional: Set the take profit level (in points)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,  # TRADE_ACTION_DEAL tells the platform that we want to open a trade 
        "symbol": "EURUSD",  # specify the symbol on which you want to open a trade
        "volume": volume,  # amount of contracts you want to open
        "type": mt5.ORDER_TYPE_SELL,  # ORDER_TYPE_BUY specifies a BUY order, use mt5.ORDER_TYPE_SELL to sell
        "price": mt5.symbol_info_tick("EURUSD").bid,  # specify the price for which you want to buy
        "sl": stop_loss,  # stoploss
        "tp": take_profit,  # take profit
        "deviation": 20,  # maximum amount of slippage allowed for your market order, otherwise reject
        "magic": 100,  # unique number identifier of the order
        "comment": "sell",  # order comment
        "type_time": mt5.ORDER_TIME_GTC,  # GTC (Good-Til-Cancelled) means that the order will remain active until cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,  # Allows partial fill of order. If the rest can't be filled, it will be cancelled
    }

    result = mt5.order_send(request)

    return result

def buy_order(volume):

    # Set the order type
    order_type = mt5.ORDER_TYPE_BUY

    # Set the stop loss and take profit levels (optional)
    stop_loss = 100.0  # Stop loss level in points
    take_profit = 200.0  # Take profit level in points

    # Set the order price (optional, if not market order)
    price = mt5.symbol_info_tick(symbol).bid
    sl = 1.0  # Optional: Set the stop loss level (in points)
    tp = 2.0  # Optional: Set the take profit level (in points)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,  # TRADE_ACTION_DEAL tells the platform that we want to open a trade 
        "symbol": "EURUSD",  # specify the symbol on which you want to open a trade
        "volume": volume,  # amount of contracts you want to open
        "type": mt5.ORDER_TYPE_BUY,  # ORDER_TYPE_BUY specifies a BUY order, use mt5.ORDER_TYPE_SELL to sell
        "price": mt5.symbol_info_tick("EURUSD").ask,  # specify the price for which you want to buy
        "sl": 0.0,  # stoploss
        "tp": 0.0,  # take profit
        "deviation": 20,  # maximum amount of slippage allowed for your market order, otherwise reject
        "magic": 100,  # unique number identifier of the order
        "comment": "buy",  # order comment
        "type_time": mt5.ORDER_TIME_GTC,  # GTC (Good-Til-Cancelled) means that the order will remain active until cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,  # Allows partial fill of order. If the rest can't be filled, it will be cancelled
    }

    result = mt5.order_send(request)
    
    return result

def close_order(ticket):
    positions = mt5.positions_get()

    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.ask, 1: tick.bid}

        if pos.ticket == ticket:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_dict[pos.type],
                "price": price_dict[pos.type],
                "magic": 100,
                "comment": "python close order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            order_result = mt5.order_send(request)
            print(order_result)

            return order_result

    return 'Ticket does not exist'


def buy(volume):
    symbol = "EURUSD"  # Replace with the desired symbol
    order_type = mt5.ORDER_TYPE_BUY
    volume = 0.1       # Replace with the desired volume/lot size
    price = mt5.symbol_info_tick(symbol).ask  # Use the current ask price as the order price
    stop_loss = price - 0.0025  # Replace with the desired stop loss price
    take_profit = price + 0.0025  # Replace with the desired take profit price

    request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": volume,
    "type": order_type,
    "price": price,
    "sl": stop_loss,
    "tp": take_profit,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order placement failed. Error code:", result.retcode)
    else:
        print("Buy order placed successfully. Order ticket:", result.order)

    return result


def buyLimit():
    symbol = "EURUSD"  # EUR/USD currency pair
    order_type = mt5.ORDER_TYPE_BUY_LIMIT
    volume = 0.1       # Replace with the desired volume/lot size
    price = mt5.symbol_info_tick(symbol).ask    # Set the price for the Buy Limit order
    stop_loss = price - 0.0025  # Replace with the desired stop loss price
    take_profit = price + 0.0025  # Replace with the desired take profit price
    request = {
    "action": mt5.TRADE_ACTION_PENDING,
    "symbol": symbol,
    "volume": volume,
    "type": order_type,
    "price": price,
    "sl":stop_loss,
    "tp":take_profit,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order placement failed. Error code:", result.retcode)
    else:
        print("Buy Limit order placed successfully. Order ticket:", result.order)


def sellStop():
    symbol = "EURUSD"  # Replace with the desired symbol
    order_type = mt5.ORDER_TYPE_SELL_STOP
    volume = 0.1       # Replace with the desired volume/lot size
    price = mt5.symbol_info_tick(symbol).ask - 0.0025
    stop_loss = price + 0.0025  # Replace with the desired stop loss price
    take_profit = price - 0.0025  # Replace with the desired take profit price

    request = {
    "action": mt5.TRADE_ACTION_PENDING,
    "symbol": symbol,
    "volume": volume,
    "type": order_type,
    "price": price,
    "sl": stop_loss,
    "tp": take_profit,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order placement failed. Error code:", result.retcode)
    else:
        print("Sell Stop order placed successfully. Order ticket:", result.order)


print(mt5.symbol_info_tick(symbol).ask)
    
   
#buyLimit()

#buy_order(0.06)

'''while True:
    # Request the last tick for the symbol
    last_tick = mt5.symbol_info_tick(symbol)
    ticket_numbers = []
    # Get the list of positions on symbols whose names contain "*USD*"
    usd_positions = mt5.positions_get(group="*USD*")
    # Extract the ticket numbers from the positions list
    ticket_numbers = [position.ticket for position in usd_positions]
           
    
    if(last_tick.ask == 1.1223 and one_sell == False):    
        sell_order(volume = 0.06)
        one_sell = True

    if(last_tick.ask == 1.1198):
        for k in range(len(ticket_numbers)):
            ticket_to_find = ticket_numbers[k]
            comment = None
            for position in usd_positions:
                if position.ticket == ticket_to_find:
                    comment = position.comment 
                    if(comment == "sell"):                   
                        close_order(ticket_numbers[k])
                        buy_order(volume = 0.06)
                        buy = True
                        one_sell = False

    if(last_tick.ask == 1.1248 or last_tick.ask == 1.1173):
        for k in range(len(ticket_numbers)):
            ticket_to_find = ticket_numbers[k]
            comment = None
            for position in usd_positions:
                if position.ticket == ticket_to_find:
                    comment = position.comment 
                    if(comment == "sell"):                   
                        close_order(ticket_numbers[k])
                        one_sell = False

    if(last_tick.ask == 1.1223 and one_sell == False and buy == True):
         for k in range(len(ticket_numbers)):
            ticket_to_find = ticket_numbers[k]
            comment = None
            for position in usd_positions:
                if position.ticket == ticket_to_find:
                    comment = position.comment 
                    if(comment == "buy"):                   
                        close_order(ticket_numbers[k])
                        one_buy = False


    #print(len(ticket_numbers))
    print(one_sell)'''
mt5.shutdown()