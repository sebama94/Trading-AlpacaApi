class Backtester:
    def __init__(self, api_key, secret_key, symbol, strategy):
        self.api = tradeapi.REST(api_key, secret_key, api_version='v2')
        self.symbol = symbol
        self.strategy = strategy

    def backtest(self, data):
        for i, price in enumerate(data):
            signal = self.strategy(data[:i+1])
            if signal == 'buy':
                self.api.submit_order(
                    symbol=self.symbol,
                    qty=1,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
            elif signal == 'sell':
                self.api.submit_order(
                    symbol=self.symbol,
                    qty=1,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
