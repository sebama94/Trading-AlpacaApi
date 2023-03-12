import time
from threading import Thread, Lock
import alpaca_trade_api as tradeapi


class Closure(Thread):
    def __init__(self, symbol, api, mutex=Lock()):
        super().__init__()
        self.api = api
        self.symbol = symbol
        self.account = self.api.get_account()
        self.mutex = mutex

    def close_positions(self):
        positions = self.api.list_positions()
        for position in positions:
            if float(position.unrealized_intraday_pl) > 2:
                    self.api.close_position(position.symbol)
                    print(f"Posizione di {position.symbol} chiusa con profitto {position.unrealized_intraday_pl}")

    def start(self):
        print(f"The closure starts now for the symbols {self.symbol}")
        while True:
            self.close_positions()
            time.sleep(0.2)


