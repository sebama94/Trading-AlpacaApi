from Utilies.utilies import dict_credential, data_analysing
from package.Deployer import Deployment
from package.Closure import Closure
import tensorflow as tf
from threading import Lock
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
START_DATA = data_analysing["START_DATA"]
END_DATA = data_analysing["END_DATE"]

# Create API object
global_mutex = Lock()

if __name__ == '__main__':
    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
    symbols_crypto = []
    symbols_shares = ["AMZN","AAPL","GOOGL","MSFT","ADT","TSLA", "NVDA", "ARM", "T", "NEE","NIO","SPCE","NKLA","PFE"]
   # symbols_shares = ["NIO","SPCE","NKLA","LCID", "H","ADT","PFE"]
    symbol_closure = symbols_crypto+symbols_shares

    thread_depoly_lists_shares  =   []
    thread_depoly_lists_cryptos =   []
    # thread_closure_lists        =   []

#    for symbol in symbols_crypto:
#       with tf.device('/device:GPU:0'):
#          deployment_crypto = DeployementCrypto(symbol, api, mutex=global_mutex, time_to_sleep = )
#         thread_depoly_lists_cryptos.append(deployment_crypto)

    for index,symbol in enumerate(symbols_shares):
        with tf.device('/device:GPU:0'):
            deployment_share = Deployment(symbol, api, mutex=global_mutex, time_to_sleep=index+1,
                                          data_start_analyze=START_DATA, data_end_amalyze=END_DATA)
            thread_depoly_lists_shares.append(deployment_share)

    closure = Closure(api=api, mutex=global_mutex)


  #  for thread_depoly_list in thread_depoly_lists_cryptos:
   #     thread_depoly_list.start()

    for thread_depoly_list in thread_depoly_lists_shares:
        thread_depoly_list.start()

    closure.start()





