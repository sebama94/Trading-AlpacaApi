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

    def start(self):
        while True:
            print(f"Closure prima del mutex")
            self.mutex.acquire()
            print(f"Closure dopo del mutex")
            try:
                print(f"Closure dopo del try")
                self.check_and_close_positions()
            finally:
                self.mutex.release()
                time.sleep(10)


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
            print("Total unrealized P/L is positive. Closing all positions.")
            # Fetch updated list of open positions
            #positions = self.api.list_positions()
            self.alpaca_trade_api.close_position(pos.symbol)
            return
        # Close individual positions that are in profit
        positions = self.alpaca_trade_api.list_positions()
        for pos in positions:
            unrealized_pl = float(pos.unrealized_pl)
            print(f"The unrealized position is  {unrealized_pl}.")
            if unrealized_pl > 100:
                print(f"Closing position for {pos.symbol} which is in profit.")
                self.alpaca_trade_api.close_position(pos.symbol)
                return
        print("Total unrealized P/L is not positive. Not closing all positions.")


