from package.DataProcessor import DataProcessor
import numpy as np
from package.ModelSelector import ModelSelector
from package.ModelTrainer import ModelTrainer
import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame, TimeFrameUnit

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
        data = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(1, TimeFrameUnit.Day), start='1980-01-01', end='2023-02-10', adjustment='raw')
        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        return closing_price

    def create_model(self):
        # Create and train model
        model_selector = ModelSelector(input_shape=1)
        model = model_selector.model

        data_processor = DataProcessor(self.collect_data())
        train_data, test_data = data_processor.split_data()

        x_train = np.array(train_data[:-1]).reshape(-1, 1)
        y_train = np.array(train_data[1:]).reshape(-1, 1)
        x_test = np.array(test_data[:-1]).reshape(-1, 1)
        y_test = np.array(test_data[1:]).reshape(-1, 1)


        model_trainer = ModelTrainer(model, x_train= x_train, y_train=y_train, x_test=x_test, y_test=y_test)
        model_trainer.train_model(epochs=200, batch_size=64)
        #plot_model(model, to_file='model.png', show_shapes=True)
        model_trainer.plot()
        return model

    def deploy_model(self):
        # Deploy model
        model = self.create_model()

        # Get current price
        current_price = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(1, TimeFrameUnit.Day),
                                                       start='2023-01-01', end='2023-12-31',adjustment='raw')[-1].c

       # current_price = self.alpaca_trade_api.get_bars(self.symbol, timeframe=TimeFrame(1, TimeFrameUnit.Day),
       #                                             adjustment='raw')[-1].c
        print("current price ", current_price)
        # Make prediction
        prediction = model.predict(np.array([[current_price]]))

        # Place order
        if prediction > current_price:
            self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='buy', type='market', time_in_force='gtc')
            print(f"Buy order placed for {self.symbol}.")
        else:
            self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='sell', type='market', time_in_force='gtc')
            print(f"Sell order placed for {self.symbol}.")
