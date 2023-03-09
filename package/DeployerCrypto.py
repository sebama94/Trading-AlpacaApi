from package.Deployer import Deployment
from alpaca_trade_api import TimeFrame, TimeFrameUnit
import time

class DeployementCrypto(Deployment):
    def __init__(self, symbol, api):
        Deployment.__init__(self, symbol, api)

    def collect_data(self):
        data = self.alpaca_trade_api.get_crypto_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute),
                                                        start='2023-03-01', end='2023-03-08')


        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        return closing_price