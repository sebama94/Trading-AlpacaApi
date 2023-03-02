from Utilies.utilies import dict_credential
from package.Deployer import Deployment
from package.Closure import Closure
import tensorflow as tf
import threading
import time
import alpaca_trade_api as tradeapi


# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())

physical_devices = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(physical_devices))


# Set API credentials
API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]

# Create API object
# api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')


def thread_main(api_key, secret_key, apca_api_base_url, symbol):
    with tf.device('/device:GPU:0'):
        # Create deployment object
        deployment = Deployment(api_key, secret_key, apca_api_base_url, symbol)

        # Deploy model
        deployment.deploy_model()

def thread_closure(api_key, secret_key, apca_api_base_url, symbol):

    closure = Closure(api_key, secret_key, apca_api_base_url, symbol)
    closure.close_positions()


#if __name__ == '__main__':
api_key = API_KEY
secret_key = API_SECRET
apca_api_base_url = APCA_API_BASE_URL
symbol = "AAPL"

alpaca_trade_api = tradeapi.REST(api_key, secret_key, apca_api_base_url, api_version='v2')

thread_closure(api_key, secret_key, apca_api_base_url, symbol, alpaca_trade_api)
thread_main(api_key, secret_key, apca_api_base_url, symbol)

thread2 = threading.Thread(target=thread_main)
thread1 = threading.Thread(target=thread_closure)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
