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

def thread_main(symbol, api):
    with tf.device('/device:GPU:0'):
        # Create deployment object
        deployment = Deployment(symbol, api)
        # Deploy model
        deployment.deploy_model()

def thread_closure(symbol, api):
    closure = Closure(symbol, api)
    closure.close_positions()


if __name__ == '__main__':
    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
    symbols = ["AAPL", "AMZN", "NKLA"]
    thread_depoly_lists=[]
    thread_closure_lists=[]
    for symbol in symbols:

        thread_depoly_lists.append(threading.Thread(target=thread_main, args=(symbol, api, )))
        thread_closure_lists.append(threading.Thread(target=thread_closure, args=(symbol, api, )))

    for thread_depoly_list in thread_depoly_lists:
        thread_depoly_list.start()
        thread_depoly_list.join()

    for thread_closure_list in thread_closure_lists:
        thread_closure_list.start()
        thread_closure_list.join()