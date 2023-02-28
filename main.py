from Utilies.utilies import dict_credential
from package.Deployer import Deployment
import os
import tensorflow as tf

import tensorflow as tf

physical_devices = tf.config.list_physical_devices('/GPU:0')
print("Num GPUs Available: ", len(physical_devices))

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# Set API credentials
API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]

# Create API object
# api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

def main(api_key, secret_key, apca_api_base_url, symbol):
    # with tf.device('/GPU:0'):
        # Create deployment object
        deployment = Deployment(api_key, secret_key, apca_api_base_url, symbol)

        # Deploy model
        deployment.deploy_model()




if __name__ == '__main__':
    api_key = API_KEY
    secret_key = API_SECRET
    apca_api_base_url = APCA_API_BASE_URL
    symbol = "AMZN"

    main(api_key, secret_key, apca_api_base_url, symbol)
