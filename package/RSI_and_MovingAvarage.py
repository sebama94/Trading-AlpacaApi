class RSIMAStrategy:
    def __init__(self,):
        self.df = None
    def fetch_data(self, data):
        self.df = data
    def refresh_latest_bars(self, data):
        self.df = self.df.append(data)

    def calculate_indicators(self):
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.df['rsi'] = 100 - (100 / (1 + rs))
        self.df['moving_avg'] = self.df['close'].rolling(window=20).mean()

    def execute_trades(self) -> str:
        for i in range(1, len(self.df)):
            print(f"Rsi is {self.df['rsi'][i]} and moving avg is {self.df['moving_avg'][i]}")
            if self.df['rsi'][i] < 30 and self.df['close'][i] > self.df['moving_avg'][i]:
                print("Buy")
                return "Buy"
            elif self.df['rsi'][i] > 70 and self.df['close'][i] < self.df['moving_avg'][i]:
                print("Sell")
                return "Sell"

    def comupteStrategy(self) -> str:
        self.calculate_indicators()
        return self.execute_trades()
