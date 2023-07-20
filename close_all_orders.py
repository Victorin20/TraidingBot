import MetaTrader5 as mt5

def close_all_orders():
    # Connect to MetaTrader 5
    if not mt5.initialize():
        print("Failed to initialize MetaTrader 5.")
        return

    # Request all open positions/orders
    positions = mt5.positions_get()

    # Close each open position/order
    for position in positions:
        ticket = position.ticket
        result = mt5.order_send(ticket, action=mt5.ORDER_ACTION_CLOSE)
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Order {ticket} closed successfully.")
        else:
            print(f"Failed to close order {ticket}. Error code: {result.retcode}, reason: {result.reason}")

    # Shutdown the MetaTrader 5 connection
    mt5.shutdown()

if __name__ == "__main__":
    close_all_orders()