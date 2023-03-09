from package.Deployer import Deployment
from alpaca_trade_api import TimeFrame, TimeFrameUnit
import time
import numpy as np


class DeployementCrypto(Deployment):
    def __init__(self, symbol, api):
        Deployment.__init__(self, symbol, api)

    def deploy_model(self):
        try:
            # real_price = float(self.alpaca_trade_api.get_position(self.symbol).current_price)
            real_price = float(self.alpaca_trade_api.get_crypto_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute))[-1].c)
            # Make prediction
            prediction = self.model.predict(np.array([[real_price]]))
            print(f"prediction {prediction} real price {real_price}")
            self.submit_order(prediction=prediction, real_price= real_price)
            time.sleep(20)
        except Exception as exception:
            print(f"[ERROR] exception {exception}. Symbol {self.symbol}")
            time.sleep(2)
            # real_price = 140

    def collect_data(self):
        data = self.alpaca_trade_api.get_crypto_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute),
                                                        start='2023-03-01', end='2023-03-08')


        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        return closing_price