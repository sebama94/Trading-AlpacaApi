import alpaca_trade_api as tradeapi

# Set API credentials
API_KEY = 'PKGDRTI7SOIC0NKE9LOB'
API_SECRET = 'GcFBmEmMmlrqPYUv4lVV8ZgqnB8VAD8bwgBLlmOc'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

# Create API object
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL)

# Define stock to buy and quantity
symbol = 'AAPL'
quantity = 10



# Buy the stock
api.submit_order(
    symbol=symbol,
    qty=quantity,
    side='buy',
    type='market',
    time_in_force='gtc'
)

# Define stock to sell and quantity
symbol = 'AAPL'
quantity = 10

# Sell the stock
api.submit_order(
    symbol=symbol,
    qty=quantity,
    side='sell',
    type='market',
    time_in_force='gtc'
)
