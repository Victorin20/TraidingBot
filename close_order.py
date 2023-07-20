# close order

import MetaTrader5 as mt5
mt5.initialize()


position = mt5.positions_get(ticket=50545533085)[0]
print(position)

tick = mt5.symbol_info_tick("EURUSD")

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "position": position.ticket,
    "symbol": position.symbol,
    "volume": position.volume,
    "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
    "price": tick.ask if position.type == 1 else tick.bid,  
    "deviation": 20,
    "magic": 100,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

result = mt5.order_send(request)
result