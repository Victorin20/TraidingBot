import MetaTrader5 as mt5
import pandas as pd


mt5.initialize()

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

# Select the desired symbol
symbol = "EURUSD"

# Request the last tick for the symbol
last_tick = mt5.symbol_info_tick(symbol)

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
                    close_order(ticket_numbers[k])
          
mt5.shutdown()