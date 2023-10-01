import time
from threading import Thread, Lock
import alpaca_trade_api as tradeapi


class Closure(Thread):
    def __init__(self, api, mutex):
        super().__init__()
        self.alpaca_trade_api = api
#        self.symbol = symbol
        self.account = self.alpaca_trade_api.get_account()
        self.mutex = mutex

    def check_and_close_positions(self):
        # Fetch open positions
        positions = self.alpaca_trade_api.list_positions()

        # Check if there are no open positions
        if not positions:
            print("No open positions.")
            return

        # Initialize total P/L
        total_pl = 0.0

        # Loop through each position to check individual P/L
        for pos in positions:
            total_pl += float(pos.unrealized_pl)
            # Check condition for closing all remaining positions
        if total_pl > 100:
           # print("Total unrealized P/L is positive. Closing all positions.")
            # Fetch updated list of open positions
            # positions = self.api.list_positions()
            self.alpaca_trade_api.close_position(pos.symbol)
            return

        #print("Total unrealized P/L is not positive. Not closing all positions.")
        # Close individual positions that are in profit
        time.sleep(3)
        positions = self.alpaca_trade_api.list_positions()
        # Check if there are no open positions
        if not positions:
            print("No open positions.")
            return

        for pos in positions:
            unrealized_pl = float(pos.unrealized_pl)
            #print(f"The symbol {pos.symbol} have unrealized position equal to {unrealized_pl}.")
            if unrealized_pl > 50:
              #  print(f"Closing position for {pos.symbol} which is in profit.")
                self.alpaca_trade_api.close_position(pos.symbol)
    def waiting_market(self):
        while True:
            clock = self.alpaca_trade_api.get_clock()
            if clock.is_open:
                # print("The market is open.")
                break
            else:
                print("The market is closed. Waiting...")
                time_to_open = clock.next_open
                sleep_time = time_to_open.total_seconds()  # Sleep half the time remaining to market open
                time.sleep(sleep_time)

    def start(self):
        while True:
            self.waiting_market()
            self.mutex.acquire()
            try:
                self.check_and_close_positions()
            finally:
                self.mutex.release()
                time.sleep(10)



