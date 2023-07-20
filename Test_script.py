import MetaTrader5 as mt5

mt5.initialize()

# Select the desired symbol
symbol = "EURUSD"
one_sell = False
one_buy = False

# Request the last tick for the symbol
last_tick = mt5.symbol_info_tick(symbol)

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


while(True):
    if(last_tick.ask >= 1.12070 and last_tick.ask <= 1.12085 and one_sell == False):
        sellStop()
        one_sell = True

print(last_tick.ask)

mt5.shutdown()