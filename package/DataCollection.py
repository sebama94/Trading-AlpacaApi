import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame, TimeFrameUnit
class DataCollector:
    def __init__(self, api_key, secret_key, apca_api_base_url):
        self.api = tradeapi.REST(api_key, secret_key, apca_api_base_url, api_version='v2')

    def collect_data(self, symbol, timeframe, limit):
        #barset = self.api.get_barset(symbol, timeframe, limit=limit)
        barset = self.api.get_bars(self.symbol, timeframe=TimeFrame(1, TimeFrameUnit.Minute), start='2020-01-01',
                              end='2020-12-31')
        bars = barset
        return [bar.c for bar in bars]
