import MetaTrader5 as mt5
import pandas as pd

pd.set_option('display.max_columns', 500)  # number of columns to be displayed
pd.set_option('display.width', 1500)       # max table width to display

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Get the list of positions on symbols whose names contain "*USD*"
usd_positions = mt5.positions_get(group="*USD*")
if usd_positions is None:
    print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
elif len(usd_positions) > 0:
    print("positions_get(group=\"*USD*\")={}".format(len(usd_positions)))
    # Get the comment of a specific ticket (replace 123456 with the desired ticket number)
    ticket_to_find = 123456
    comment = None
    for position in usd_positions:
        if position.ticket == ticket_to_find:
            comment = position.comment
            break

    if comment:
        print(f"Comment of ticket {ticket_to_find}: {comment}")
    else:
        print(f"No position found with ticket number {ticket_to_find}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
