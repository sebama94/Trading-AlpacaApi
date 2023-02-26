import alpaca_trade_api as tradeapi
from Utilies.utilies import dict_credential
from  alpaca_trade_api import TimeFrame, TimeFrameUnit, REST
# Set API credentials
API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]



# Create API object
# Create API client instance
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
print(api)
# Specify the stock and date range for the historical data
symbol = 'AAPL' # Replace with the symbol of the stock you want to get historical data for
start_date = '2022-01-01'
end_date = '2022-01-08'

# Get the historical price data for the specified stock and date range
barset = api.get_bars(symbol, timeframe=TimeFrame(1, TimeFrameUnit.Day),start='2020-12-31', end='2020-12-31', adjustment='raw')

# Extract the closing prices from the historical price data

print(barset)
stock_bars = barset
closing_prices = [bar.c for bar in stock_bars]
print(closing_prices)
