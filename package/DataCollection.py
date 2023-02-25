import alpaca_trade_api as tradeapi

class DataCollector:
    def __init__(self, api_key, secret_key):
        self.api = tradeapi.REST(api_key, secret_key, api_version='v2')

    def collect_data(self, symbol, timeframe, limit):
        barset = self.api.get_barset(symbol, timeframe, limit=limit)
        bars = barset[symbol]
        return [bar.c for bar in bars]
