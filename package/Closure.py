import time

import alpaca_trade_api as tradeapi

class Closure:
    def __init__(self, symbol, api):
        self.api = api
        self.symbol = symbol
        self.account = self.api.get_account()

    def close_positions(self):
        while True:
            positions = self.api.list_positions()
            for position in positions:
                if float(position.unrealized_intraday_pl) > 0:
                    self.api.close_position(position.symbol)
                    print(f"Posizione di {position.symbol} chiusa con profitto")

            time.sleep(2)
