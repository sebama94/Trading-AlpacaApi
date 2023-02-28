import pandas as pd
import time
from package.DataProcessor import DataProcessor
import numpy as np
from package.ModelSelector import ModelSelector
from package.ModelTrainer import ModelTrainer
import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame, TimeFrameUnit
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(physical_devices))

class Deployment:
    def __init__(self, api_key, secret_key, apca_api_base_url, symbol):
        self.api_key = api_key
        self.secret_key = secret_key
        self.apca_api_base_url = apca_api_base_url
        self.symbol = symbol
        self.alpaca_trade_api = tradeapi.REST(self.api_key, self.secret_key, self.apca_api_base_url, api_version='v2')
        self.length_batch = None

    def collect_data(self):
        # Collect data
        data = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute),
                                              start='2023-02-21', end='2023-02-26', adjustment='raw')

        print(data)
        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        print(closing_price)
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
        #plot_model(model, to_file='model.png', show_shapes=True)
        model_trainer.plot()
        return model

    def deploy_model(self):
        # Deploy model
        model = self.create_model()

        # Get current price
        # current_price = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(1, TimeFrameUnit.Day),
        #                                                start='2023-01-01', end='2023-02-10' ,adjustment='raw')[-1].c

        # current_price = float(self.alpaca_trade_api.get_last_trade(self.symbol).price)

        now = pd.Timestamp.now(tz='Europe/Rome').floor('1min')
        today = now.strftime('%Y-%m-%d')
        tomorrow = (now - pd.Timedelta('1day')).strftime('%Y-%m-%d')

        # real_price = self.alpaca_trade_api.get_bars( self.symbol, timeframe=TimeFrame(1, TimeFrameUnit.Hour),
        # #                                                 start="2023-02-01", end="2023-02-26", adjustment='raw' )
        # current_price = [bar.c for bar in real_price]
        # self.length_batch = len(current_price)
        # print(self.length_batch)
        while True:
            print("sono qui ")
            # //print(self.alpaca_trade_api.get_position(self.symbol))
            try:
                real_price = float(self.alpaca_trade_api.get_position(self.symbol).current_price)
            except Exception as exception:
                if exception.__str__() == 'position does not exist':
                    print("exception")
                    real_price = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(15, TimeFrameUnit.Minute),
                                              start='2023-02-21', end='2023-02-26', adjustment='raw')[-1].c
            # Make prediction
            prediction = model.predict(np.array([[real_price]]))
            print(f"prediction {prediction} real price {real_price}")

            # Place order
            #
            if prediction > real_price:
                # self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='buy', type='market', time_in_force='gtc')
                print(f"Buy order placed for {self.symbol}.")
            else:
                # self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='sell', type='market', time_in_force='gtc')
                print(f"Sell order placed for {self.symbol}.")

            time.sleep(20)
