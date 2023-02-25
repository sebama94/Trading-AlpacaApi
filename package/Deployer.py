from package.DataProcessor import DataProcessor
import numpy as np
from package.ModelSelector import ModelSelector
from package.ModelTrainer import ModelTrainer

class Deployment:
    def __init__(self, api_key, secret_key, symbol):
        self.api_key = api_key
        self.secret_key = secret_key
        self.symbol = symbol

    def collect_data(self):
        # Collect data
        api = tradeapi.REST(self.api_key, self.secret_key, api_version='v2')
        data = api.get_barset(self.symbol, 'day', limit=200)[self.symbol].df['close'].values
        return data

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

        model_trainer = ModelTrainer(model, x_train, y_train)
        model_trainer.train_model()
        return model

    def deploy_model(self):
        # Deploy model
        model = self.create_model()
        alpaca_trade_api = tradeapi.REST(self.api_key, self.secret_key, api_version='v2')

        # Get current price
        current_price = float(alpaca_trade_api.get_last_trade(self.symbol).price)

        # Make prediction
        prediction = model.predict(np.array([[current_price]]))

        # Place order
        if prediction > current_price:
            alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='buy', type='market', time_in_force='gtc')
            print(f"Buy order placed for {self.symbol}.")
        else:
            alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='sell', type='market', time_in_force='gtc')
            print(f"Sell order placed for {self.symbol}.")
