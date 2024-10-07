import os.path
import time

import pytz
from keras.models import load_model
from package.DataProcessor import DataProcessor
import numpy as np
from package.ModelSelector import ModelSelector
from package.ModelTrainer import ModelTrainer
import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame, TimeFrameUnit
from threading import Thread, Condition
from requests.exceptions import HTTPError
from datetime import datetime
from package.RSI_and_MovingAvarage import RSIMAStrategy

class Deployment(Thread):
    def __init__(self, symbol, api, mutex, time_to_sleep, data_start_analyze, data_end_amalyze):
        Thread.__init__(self, daemon=True)
        self.symbol = symbol
        self.alpaca_trade_api = api
        self.length_batch = None
        self.model = None
        self.mutex = mutex
        self.daemon = True
        self.time_to_sleep = time_to_sleep
        # self.rsi_and_avarage = RSIMAStrategy()
        self.data_start_analyze = data_start_analyze
        self.data_end_amalyze = data_end_amalyze

    def check_investment(self) -> bool:
        # Ottieni il valore totale del portafoglio
        account = self.alpaca_trade_api.get_account()
        #print(f"account value {account}")

        total_equity = float(account.equity)  # Capitale totale
        # Ottieni la posizione attuale per l'asset specifico
        try:
            position = self.alpaca_trade_api.get_position(self.symbol)
        #    print(f"capitale totale {total_equity}")
        except Exception as e:
            print(f"Errore nel recuperare la posizione: {e}")
            #return False

        asset_value = float(position.market_value)  # Valore investito nell'asset
        #print(f"account value {account} e capitale totale {total_equity} e asset value {asset_value}")
        # Controlla se l'importo investito è maggiore del 10% del capitale totale
        compute = asset_value / total_equity
        print(f"the percentage is  {compute} \n")#e capitale totale {total_equity} e asset value {asset_value}")
        if compute > 0.1:
            return False
        else:
            return True

    def __del__(self):
        print("Close program")
    def collect_data(self):
        # Collect data
        data = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(5, TimeFrameUnit.Minute),
                                              start=self.data_start_analyze, end=self.data_end_amalyze, adjustment='raw')
        # self.rsi_and_avarage.fetch_data(data=data)
        closing_price = [bar.c for bar in data]
        self.length_batch = len(closing_price)
        return closing_price

    def create_model(self):
        # Create and train model
      #  print(f"il modello che sto creando è per il simbolo {self.symbol}")
        data_processor = DataProcessor(self.collect_data())
        train_data, test_data = data_processor.split_data()
        x_train = np.array(train_data[:-1]).reshape(-1, 1)
        y_train = np.array(train_data[1:]).reshape(-1, 1)
        x_test = np.array(test_data[:-1]).reshape(-1, 1)
        y_test = np.array(test_data[1:]).reshape(-1, 1)
        model_selector = ModelSelector(X_train=x_train)
        model = model_selector.model
        model_trainer = ModelTrainer(model, x_train= x_train, y_train=y_train, x_test=x_test, y_test=y_test)
        model_trainer.train_model(epochs=30, batch_size=32)
        self.model = model
        # print(f"Saving model {self.symbol}")
        # model.save("model/"+self.symbol+".h5")

    def deploy_model(self):
        real_price = self.get_bars()
        prediction = self.model.predict(np.array([[real_price]]))
        qty = self.get_quantity()
        if qty is None:
            quantity = 0
        else:
            quantity = float(qty)
        self.submit_order(prediction=prediction, real_price=real_price, quantity=quantity)

    def get_bars(self):
        try:
            data = self.alpaca_trade_api.get_bars(self.symbol, timeframe= TimeFrame(5, TimeFrameUnit.Minute)).df.iloc[0]
            # self.rsi_and_avarage.refresh_latest_bars(data=data)
           # print(f"this is data {data}")
            return float(data['close'])
        except Exception as exception:
            print(f"[ERROR] exception {exception}. Symbol {self.symbol}")
            return 0

    def submit_order(self, prediction, real_price, quantity):
        # rsi_avg = self.rsi_and_avarage.comupteStrategy()
        try:
            if prediction > real_price+0.01 and quantity >= 0: # and rsi_avg == "Buy":
                self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='buy', type='market',
                                                   time_in_force='gtc')
                print(f"Buy order placed for {self.symbol} at predicted price: {prediction} > real: {real_price} and quantity {quantity}")
            elif prediction < real_price-0.01 and quantity <= 0: # and rsi_avg == "Sell":
                self.alpaca_trade_api.submit_order(symbol=self.symbol, qty=1, side='sell', type='market',
                                                   time_in_force='gtc')
                print(f"Sell order placed for {self.symbol} at predicted price: {prediction} < real: {real_price} and quantity {quantity}")
        except Exception as exception:
            print(f"[ERROR] exception submit_order {exception}. Symbol {self.symbol}")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

    def get_quantity(self):
        try:
            position = self.alpaca_trade_api.get_position(self.symbol)
            qty = position.qty  # This will give you the quantity of your position, positive for long and negative for short
            #print(f"The quantity of the position for {self.symbol} is {qty}.")
            return float(qty)
        except tradeapi.rest.APIError as e:
            print(f"An error occurred: {e}")
            return float(0)

    def waiting_market(self):
        while True:
            clock = self.alpaca_trade_api.get_clock()
            if clock.is_open:
             #   print("The market is open.")
                break
            else:
                condition = Condition()
                with condition:
                    future_timestamp_str = clock.next_open
                    # Convert the string to a datetime object, taking into account the time zone
                    future_dt_object = datetime.fromisoformat(str(future_timestamp_str))
                    # Convert future time to UTC
                    future_utc_dt_object = future_dt_object.astimezone(pytz.UTC)
                    # Get current UTC time
                    current_utc_dt_object = datetime.now(pytz.UTC)
                    # Calculate the difference in seconds
                    time_to_open = (future_utc_dt_object - current_utc_dt_object).total_seconds()
                    print(f"The market is closed. Waiting... {time_to_open} seconds")
                    condition.wait(timeout=time_to_open)
                    print(f"Condition")

    def run(self):
        print(f"sto inizio l'escutionze {self.symbol}\n")
        self.create_model()
        while True:
            self.waiting_market()
            self.mutex.acquire()
            try:
                self.deploy_model()
            finally:
                self.mutex.release()
                time.sleep(self.time_to_sleep+301)