from package.Deployer import Deployment
from alpaca_trade_api import TimeFrame, TimeFrameUnit
import time
import numpy as np
from threading import Thread


class DeployementCrypto(Deployment):
    def __init__(self, symbol, api, mutex):
        Deployment.__init__(self, symbol, api, mutex=mutex)
        Thread.__init__(self, daemon=True)
    def get_bars(self):
        try:
            return float(self.alpaca_trade_api.get_crypto_bars(self.symbol, timeframe= TimeFrame(1, TimeFrameUnit.Minute))[-1].c)
        except Exception as exception:
            print(f"[ERROR] exception {exception}. Symbol {self.symbol}")
            time.sleep(1)
            return 0

    def collect_data(self):
        data = self.alpaca_trade_api.get_crypto_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute),
                                                        start='2023-09-1', end='2023-09-20')


        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        return closing_price