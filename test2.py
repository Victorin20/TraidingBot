import MetaTrader5 as mt5

mt5.initialize()

# Select the desired symbol
symbol = "EURUSD"
one_sell = False
one_buy = False

# Request the last tick for the symbol
last_tick = mt5.symbol_info_tick(symbol)

print(last_tick.ask)