import MetaTrader5 as mt5

# Connect to the MetaTrader 5 terminal

symbol = "EURUSD"

mt5.initialize()

# Define the order parameters
 # Set the order type
order_type = mt5.ORDER_TYPE_BUY

# Set the stop loss and take profit levels (optional)
stop_loss = 100.0  # Stop loss level in points
take_profit = 200.0  # Take profit level in points

volume = 0.1

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

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()