import alpaca_trade_api as tradeapi
from Utilies.utilies import dict_credential
from package.Deployer import Deployment

# Set API credentials
API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]

# Create API object
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

def main(api_key, secret_key, symbol):
    # Create deployment object
    deployment = Deployment(api_key, secret_key, symbol)

    # Deploy model
    deployment.deploy_model()


if __name__ == '__main__':
    api_key = API_KEY
    secret_key = API_SECRET
    symbol = APCA_API_BASE_URL

    main(api_key, secret_key, symbol)
