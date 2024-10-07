import backtrader as bt
from datetime import datetime
import numpy as np
from keras.models import load_model
import backtrader as bt
from datetime import datetime
import alpaca_backtrader_api
import numpy as np
from keras.models import load_model



from Utilies.utilies import dict_credential, data_analysing
from package.Deployer import Deployment
from package.Closure import Closure
import tensorflow as tf
from threading import Lock
import alpaca_trade_api as tradeapi


API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]
START_DATA = data_analysing["START_DATA"]
END_DATA = data_analysing["END_DATE"]
class MLAndClosureStrategy(bt.Strategy):
    params = (
        ('profit_threshold', 5),  # The profit at which we close positions
    )

    def __init__(self):
        # Machine Learning model
        self.model = load_model('path_to_your_model.h5')
        self.data_live = False

    def notify_data(self, data, status, *args, **kwargs):
        if status == data.LIVE:
            self.data_live = True

    def next(self):
        if not self.data_live:
            return  # We are not live yet, no new data to process

        # ML Strategy Logic
        # Here you would implement the logic to make predictions using your ML model
        # and decide whether to buy or sell based on those predictions.
        # For example:
        real_price = self.data.close[0]  # Current closing price
        prediction = self.model.predict(np.array([[real_price]]))

        if prediction > real_price:
            self.buy(size=1)
        elif prediction < real_price:
            self.sell(size=1)

        # Closure Strategy Logic
        # Here you would implement the logic to check each position
        # and close it if it has reached a certain profit threshold.
        # For example:
        for data in self.datas:
            position = self.getposition(data)
            if position.size:
                unrealized_pl = position.size * (data.close[0] - position.price)
                if unrealized_pl > self.params.profit_threshold:
                    print(f"Time {datetime.now()} | Closing position {data._name}. Profit: {unrealized_pl}")
                    self.close(data)  # Close the position



# Define your MLAndClosureStrategy incorporating the logic from Deployment and Closure



# Add initialization logic, including loading your model
# Add next method logic for making predictions and closing profitable positions

# Define your main execution logic
if __name__ == '__main__':
    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

    symbols_shares = ["AMZN", "AAPL", "GOOGL", "MSFT", "ADT", "TSLA", "NVDA", "ARM", "T", "NEE", "NIO", "SPCE", "NKLA",
                      "PFE"]

    # Set up Cerebro
    cerebro = bt.Cerebro()

    # Set cash
    cerebro.broker.set_cash(100000)

    # Add a strategy
    cerebro.addstrategy(MLAndClosureStrategy)

    # Add data feeds for each symbol
    for symbol in symbols_shares:
        data = alpaca_backtrader_api.AlpacaData(dataname=symbol,
                                                historical=True,
                                                fromdate=datetime(2020, 1, 1),
                                                todate=datetime(2021, 12, 31),
                                                timeframe=bt.TimeFrame.Days)
        cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    # Plot the results
    cerebro.plot()
