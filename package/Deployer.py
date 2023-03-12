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

class Deployment(Thread):
    def __init__(self, symbol, api, mutex=Lock()):
        Thread.__init__(self, daemon=True)
        self.symbol = symbol
        #self.alpaca_trade_api = tradeapi.REST(self.api_key, self.secret_key, self.apca_api_base_url, api_version='v2')
        self.alpaca_trade_api = api
        self.length_batch = None
        self.model = None
        self.mutex = mutex
        self.daemon = True
    def __del__(self):
        print("Close program")
    def collect_data(self):
        # Collect data
        data = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(1, TimeFrameUnit.Minute),
                                              start='2023-03-01', end='2023-03-08', adjustment='raw')

        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        return closing_price

    def create_model(self):
        # Create and train model
        print(f"il modello che sto creando è per il simbolo {self.symbol}")
        data_processor = DataProcessor(self.collect_data())
        train_data, test_data = data_processor.split_data()
        x_train = np.array(train_data[:-1]).reshape(-1, 1)
        y_train = np.array(train_data[1:]).reshape(-1, 1)
        x_test = np.array(test_data[:-1]).reshape(-1, 1)
        y_test = np.array(test_data[1:]).reshape(-1, 1)
        model_selector = ModelSelector(X_train=x_train)
        model = model_selector.model
        model_trainer = ModelTrainer(model, x_train= x_train, y_train=y_train, x_test=x_test, y_test=y_test)
        model_trainer.train_model(epochs=100, batch_size=64)

        self.model = model


    def deploy_model(self):
        #real_price = float(self.alpaca_trade_api.get_position(self.symbol).current_price)
        real_price = self.get_bars()
        # Make prediction
        prediction = self.model.predict(np.array([[real_price]]))
       # print(f"Symbol {self.symbol} --> Prediction {prediction} Real price {real_price}")
        self.submit_order(prediction=prediction, real_price= real_price)
        time.sleep(30)

    def get_bars(self):
        try:
            return float(self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(1, TimeFrameUnit.Minute))[-1].c)
        except Exception as exception:
            print(f"[ERROR] exception {exception}. Symbol {self.symbol}")
            return 0


    def submit_order(self, prediction, real_price):
        if prediction > real_price:
            self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='buy', type='market',
                                               time_in_force='gtc')
            print(f"Buy order placed for {self.symbol} at price of {real_price}.")
        # else:
        #     self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='sell', type='market',
        #                                        time_in_force='gtc')
        #     print(f"Sell order placed for {self.symbol} at price of {real_price}.")

    def run(self):
        print(f"sto eseguento questo thread {self.symbol}")
        self.mutex.acquire()
        try:
            self.create_model()
        finally:
            self.mutex.release()
            time.sleep(0.1)

        while True:
            self.mutex.acquire()
            try:
                self.deploy_model()
            finally:
                self.mutex.release()
                time.sleep(0.2)