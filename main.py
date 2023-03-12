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
global_mutex = Lock()


if __name__ == '__main__':
    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
    symbols_crypto = ["ETHUSD","DOGEUSD"]
    symbols_shares = []
    symbol_closure = symbols_crypto+symbols_shares

    thread_depoly_lists_shares  =   []
    thread_depoly_lists_cryptos =   []
    thread_closure_lists        =   []

    for symbol in symbol_closure:
        closure = Closure(symbol, api, mutex=global_mutex)
        thread_closure_lists.append(closure)

    for symbol in symbols_crypto:
        with tf.device('/device:GPU:0'):
            deployment_crypto = DeployementCrypto(symbol, api, mutex=global_mutex)
        thread_depoly_lists_cryptos.append(deployment_crypto)

    for symbol in symbols_shares:
        with tf.device('/device:GPU:0'):
            deployment_share = Deployment(symbol, api, mutex=global_mutex)
        thread_depoly_lists_shares.append(deployment_share)

    for thread_depoly_list in thread_depoly_lists_cryptos:
        thread_depoly_list.start()

    for thread_depoly_list in thread_depoly_lists_shares:
        thread_depoly_list.start()

    for thread_closure_list in thread_closure_lists:
        thread_closure_list.start()




