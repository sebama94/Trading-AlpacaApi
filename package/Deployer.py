import pandas as pd
import time
from package.DataProcessor import DataProcessor
import numpy as np
from package.ModelSelector import ModelSelector
from package.ModelTrainer import ModelTrainer
import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame, TimeFrameUnit
from threading import Thread, Lock
from threading import Thread, Lock

class Deployment:
    def __init__(self, symbol, api):
        self.symbol = symbol
        #self.alpaca_trade_api = tradeapi.REST(self.api_key, self.secret_key, self.apca_api_base_url, api_version='v2')
        self.alpaca_trade_api = api
        self.length_batch = None
        self.model = None


    def collect_data(self):
        # Collect data
        data = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute),
                                              start='2023-03-01', end='2023-03-08', adjustment='raw')

        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        return closing_price

    def create_model(self):
        # Create and train model
        data_processor = DataProcessor(self.collect_data())
        train_data, test_data = data_processor.split_data()
        x_train = np.array(train_data[:-1]).reshape(-1, 1)
        y_train = np.array(train_data[1:]).reshape(-1, 1)
        x_test = np.array(test_data[:-1]).reshape(-1, 1)
        y_test = np.array(test_data[1:]).reshape(-1, 1)
        model_selector = ModelSelector(X_train=x_train)
        model = model_selector.model
        model_trainer = ModelTrainer(model, x_train= x_train, y_train=y_train, x_test=x_test, y_test=y_test)
        model_trainer.train_model(epochs=50, batch_size=64)

        self.model = model


    def deploy_model(self):
        try:
            #real_price = float(self.alpaca_trade_api.get_position(self.symbol).current_price)
            real_price = float(self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute))[-1].c)
            # Make prediction
            prediction = self.model.predict(np.array([[real_price]]))
            print(f"prediction {prediction} real price {real_price}")
            self.submit_order(prediction=prediction, real_price= real_price)
            time.sleep(20)
        except Exception as exception:
            print(f"[ERROR] exception {exception}. Symbol {self.symbol}")
            time.sleep(2)
            # real_price = 140

    def submit_order(self, prediction, real_price):
        real_price = real_price
        if prediction > real_price:
            self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='buy', type='market',
                                               time_in_force='gtc')
            print(f"Buy order placed for {self.symbol}.")
        else:
            self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='sell', type='market',
                                               time_in_force='gtc')
            print(f"Sell order placed for {self.symbol}.")
