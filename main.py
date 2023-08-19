import MetaTrader5 as mt5


mt5.initialize()


startPrice = 1.08600
bet = 16
points = 0.0025

path = "C:/Users/victo/Downloads/file.txt"

# Select the desired symbol
symbol = "EURUSD"

failed = False
succes = False

f = open(path, "r")
failures = f.read()
failures = int(failures)
f.close()


# Request the last tick for the symbol
last_tick = mt5.symbol_info_tick(symbol)


def cancel_order(order_number):
    # Create the request
    request = {
        "action": mt5.TRADE_ACTION_REMOVE,
        "order": order_number,
        "comment": "Order Removed"
    }
    # Send order to MT5
    order_result = mt5.order_send(request)
    return order_result

def cancel_buyLimit_order():
    orders = mt5.orders_get(only_this_symbol=False)

    order_to_remove = None
    for order in orders:
        if order.type == mt5.ORDER_TYPE_BUY_LIMIT and order.state == mt5.ORDER_STATE_PLACED:
            order_to_remove = order
            break

    cancel_order(order_to_remove.ticket)

def cancel_SellStop_order():
    orders = mt5.orders_get(only_this_symbol=False)

    order_to_remove = None
    for order in orders:
        if order.type == mt5.ORDER_TYPE_SELL_STOP and order.state == mt5.ORDER_STATE_PLACED:
            order_to_remove = order
            break

    cancel_order(order_to_remove.ticket)

def cancel_SellLimit_order():
    orders = mt5.orders_get(only_this_symbol=False)

    order_to_remove = None
    for order in orders:
        if order.type == mt5.ORDER_TYPE_SELL_LIMIT and order.state == mt5.ORDER_STATE_PLACED:
            order_to_remove = order
            break

    cancel_order(order_to_remove.ticket)

def buyLimit(bet, position, volume):
    symbol = "EURUSD"  # EUR/USD currency pair
    order_type = mt5.ORDER_TYPE_BUY_LIMIT       # Replace with the desired volume/lot size
    price = startPrice - position * points     # Set the price for the Buy Limit order
    stop_loss = price - points  # Replace with the desired stop loss price
    take_profit = price + points  # Replace with the desired take profit price
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

def sellStop(bet, position, volume):
    symbol = "EURUSD"  # Replace with the desired symbol
    order_type = mt5.ORDER_TYPE_SELL_STOP
    price = startPrice - position * points
    stop_loss = price + points  # Replace with the desired stop loss price
    take_profit = price - points  # Replace with the desired take profit price

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

def sellLimit(bet, position, volume):
    symbol = "EURUSD"  # Replace with the desired symbol
    order_type = mt5.ORDER_TYPE_SELL_LIMIT
    price = startPrice - position * points
    stop_loss = price + points  # Replace with the desired stop loss price
    take_profit = price - points  # Replace with the desired take profit price

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



#print(mt5.symbol_info_tick(symbol).ask)
    
sellStop(bet, 0, 0.06)
buyLimit(bet*2, 1, 0.13)

first_active = True
second_active = False
third_active = False
fourd_active = False
fifth_active = False
sixth_active = False
seventh_active = False


third = False
fourd = False
fifth = False
sixth = False
seventh = False


while failed == False and succes == False:

    last_tick = mt5.symbol_info_tick(symbol)
    last_price = last_tick.ask

    if(first_active and last_price >= startPrice + points):
        failed = True
        cancel_buyLimit_order()

    if(first_active and last_price <= startPrice - points):
        first_active = False
        second_active = True

    if(second_active and last_price <= startPrice - points*2):
        failed = True
        cancel_SellLimit_order()

    if(second_active and last_price >= startPrice):
        second_active = False
        third_active = True

    if(third_active and last_price >= startPrice + points):
        failed = True
        cancel_SellStop_order()
    
    if(third_active and last_price <= startPrice - points):
        third_active = False
        fourd_active = True
    
    if(fourd_active and last_price >= startPrice):
        failed = True
        cancel_SellStop_order

    if(fourd_active and last_price <= startPrice - points*2):
        fourd_active = False
        fifth_active = True

    if(fifth_active and last_price >= startPrice - points):
        failed = True
        cancel_SellStop_order


    if(fifth_active and last_price <= startPrice - points*3):
        fifth_active = False
        sixth_active = True
    
    if(sixth_active and last_price >= startPrice - points*2):
        failed = True
        cancel_SellStop_order()

    if(sixth_active and last_price <= startPrice - points*4):
        sixth_active = False
        succes = True


    if(failed == False):

        if(last_price <= startPrice - points and third == False and second_active):    
            sellLimit(bet*4, 0, 0.26)
            third = True

        if(last_price >= startPrice and fourd == False and third_active):
            sellStop(bet*8, 1, 0.5)
            fourd = True
        
        if(last_price <= startPrice - points and fifth == False and fourd_active):
            sellStop(bet*16, 2, 1)
            fifth = True
        
        if(last_price <= startPrice - points * 2 and sixth == False and fifth_active):
            sellStop(bet*32, 3, 2.5)
            sixth = True

        if(last_price <= startPrice - points * 3 and seventh == False and sixth_active):
            sellStop(bet*64, 4, 4.1)
            seventh = True
       
if(failed):
    failures+=1

with open(path, 'w') as file:
    failures = str(failures)
    file.write(failures)

if(succes):
    print("Succes you win " + bet*64)
else : 
    print("Failed")

   
mt5.shutdown()
