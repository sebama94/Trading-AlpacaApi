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

            time.sleep(0.2)

# Inserisci qui la tua API Key e Secret Key di Alpaca

if __name__ == '__main__':
    api_key = "API Key"
    secret_key = "Secret Key"
    base_url = "https://paper-api.alpaca.markets" # URL dell'ambiente di test Alpaca

    trader = AlpacaTrader(api_key, secret_key, base_url)
    trader.close_positions()
