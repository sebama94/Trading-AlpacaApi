from Utilies.utilies import dict_credential
from package.Deployer import Deployment
from package.DeployerCrypto import DeployementCrypto

from package.Closure import Closure
import tensorflow as tf
from threading import Thread, Lock

import time
import alpaca_trade_api as tradeapi


# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())
TF_CPP_MIN_LOG_LEVEL="2"
physical_devices = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(physical_devices))


# Set API credentials
API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]

# Create API object
mutex = Lock()
def thread_deploy_cryptos(symbol, api):
    with tf.device('/device:GPU:0'):
        # Create deployment object
        deployment = DeployementCrypto(symbol, api)
        # Deploy model
        deployment.create_model()

        while True:
            mutex.acquire()
            try:
                deployment.deploy_model()
            finally:
                mutex.release()
                time.sleep(2)

def thread_deploy_shares(symbol, api):
    with tf.device('/device:GPU:0'):
        # Create deployment object
        deployment = Deployment(symbol, api)
        deployment.create_model()
        while True:
            # Deploy model
            mutex.acquire()
            try:
                deployment.deploy_model()
            finally:
                mutex.release()
                time.sleep(2)


def thread_closure(symbol, api):
    closure = Closure(symbol, api)
    closure.close_positions()

if __name__ == '__main__':
    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
    symbols_crypto = ["ETHUSD"]
    symbols_shares = ["AAPL"]

    thread_depoly_lists_shares=[]
    thread_depoly_lists_cryptos= []
    thread_closure_lists=[]

    for symbol in symbols_crypto:
        thread_depoly_lists_cryptos.append(Thread(target=thread_deploy_cryptos, args=(symbol, api, )))
        thread_closure_lists.append(Thread(target=thread_closure, args=(symbol, api, )))

    for symbol in symbols_shares:
        thread_depoly_lists_shares.append(Thread(target=thread_deploy_shares, args=(symbol, api, )))
        thread_closure_lists.append(Thread(target=thread_closure, args=(symbol, api, )))

    for thread_depoly_list in thread_depoly_lists_cryptos:
        thread_depoly_list.start()

    for thread_depoly_list in thread_depoly_lists_shares:
        thread_depoly_list.start()

    for thread_closure_list in thread_closure_lists:
        thread_closure_list.start()

