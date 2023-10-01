import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import time

from alpaca_trade_api import TimeFrame, TimeFrameUnit

from Utilies.utilies import dict_credential
# Set API credentials
API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]


class RSIMAStrategy:
    def __init__(self, symbol, api):
        self.symbol = symbol
        self.alpaca_trade_api = api
        self.df = None

    def fetch_data(self):
        self.df = self.alpaca_trade_api.get_bars(self.symbol, timeframe=TimeFrame(1, TimeFrameUnit.Minute),
                                              start='2023-09-20', end='2023-09-25', adjustment='raw')
        print(self.df)

    def calculate_indicators(self):
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.df['rsi'] = 100 - (100 / (1 + rs))
        self.df['moving_avg'] = self.df['close'].rolling(window=20).mean()

    def execute_trades(self) -> str:
        for i in range(1, len(self.df)):
            print(f"Rsi is {self.df['rsi'][i]} and moving avg is {self.df['moving_avg'][i]}")
            if self.df['rsi'][i] < 30 and self.df['close'][i] > self.df['moving_avg'][i]:
                print("Buy")
                return "Buy"
            elif self.df['rsi'][i] > 70 and self.df['close'][i] < self.df['moving_avg'][i]:
                print("Sell")
                return "Sell"


    def comupteStrategy(self) -> str:
        self.fetch_data()
        self.calculate_indicators()
        return self.execute_trades()


if __name__ == '__main__':
    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
    rsi = RSIMAStrategy(symbol="AMZN", api=api)
    stampo = rsi.comupteStrategy()
    print(stampo)