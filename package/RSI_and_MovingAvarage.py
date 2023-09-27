import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np


class RSIMAStrategy:
    def __init__(self, symbol, api):
        self.symbol = symbol
        self.api = api
        self.df = None

    def fetch_data(self):
        self.df = self.api.get_barset(self.symbol, 'day', limit=100).df[self.symbol]

    def calculate_indicators(self):
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.df['rsi'] = 100 - (100 / (1 + rs))
        self.df['moving_avg'] = self.df['close'].rolling(window=20).mean()

    def execute_trades(self) -> str:
        for i in range(1, len(self.df)):
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