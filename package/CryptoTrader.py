import alpaca_trade_api as tradeapi

from Utilies.utilies import dict_credential

API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]


class CryptoTrader:
    def __init__(self, api_key, api_secret, base_url='https://paper-api.alpaca.markets'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.api = tradeapi.REST(api_key, api_secret, base_url=base_url, api_version='v2')

    def get_account(self):
        return self.api.get_account()

    def buy_crypto(self, symbol, quantity, order_type='limit', limit_price=None):
        if order_type == 'limit' and limit_price is None:
            raise ValueError('limit_price must be specified for limit orders')
        return self.api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type=order_type,
            time_in_force='gtc',
            limit_price=limit_price,
            order_class='simple',
            asset_class='crypto'
        )

    def sell_crypto(self, symbol, quantity, order_type='limit', limit_price=None):
        if order_type == 'limit' and limit_price is None:
            raise ValueError('limit_price must be specified for limit orders')
        return self.api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type=order_type,
            time_in_force='gtc',
            limit_price=limit_price,
            order_class='simple',
            asset_class='crypto'
        )

    def get_crypto_position(self, symbol):
        return self.api.get_position(symbol, asset_class='crypto')

    def get_crypto_positions(self):
        return self.api.list_positions(asset_class='crypto')

    def get_crypto_history(self, symbol, start_date, end_date):
        return self.api.get_barset(symbol, 'day', start=start_date, end=end_date).df[symbol]

    def cancel_order(self, order_id):
        return self.api.cancel_order(order_id)
