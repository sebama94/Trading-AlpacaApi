import time
from threading import Thread, Condition
from datetime import datetime
import pytz
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

        total_pl = 0.0

        for pos in positions:
            unrealized_pl = float(pos.unrealized_pl)
            if unrealized_pl > 100:
                print(f"Closing position for {pos.symbol}. Profit: {unrealized_pl}")
                self.alpaca_trade_api.close_position(pos.symbol)
                return
            total_pl += float(pos.unrealized_pl)
        if total_pl > 1000:
            print(f"Total unrealized P/L is positive. Closing all positions. Total profit is {total_pl}")
            for pos in positions:
                self.alpaca_trade_api.close_position(pos.symbol)
            time.sleep(400)
            return
    def waiting_market(self):
        while True:
            clock = self.alpaca_trade_api.get_clock()
            if clock.is_open:
                break
            else:
                condition = Condition()
                with condition:
                    future_timestamp_str = clock.next_open
                    # Convert the string to a datetime object, taking into account the time zone
                    future_dt_object = datetime.fromisoformat(str(future_timestamp_str))
                    # Convert future time to UTC
                    future_utc_dt_object = future_dt_object.astimezone(pytz.UTC)
                    # Get current UTC time
                    current_utc_dt_object = datetime.now(pytz.UTC)
                    # Calculate the difference in seconds
                    time_to_open = (future_utc_dt_object - current_utc_dt_object).total_seconds()
                    print(f"The market is closed. Waiting... {time_to_open} seconds")
                    condition.wait(timeout=time_to_open)
                    print(f"Condition")

    def start(self):
        while True:
            self.waiting_market()
            self.mutex.acquire()
            try:
                self.check_and_close_positions()
            finally:
                self.mutex.release()
                time.sleep(30)



