import alpaca_trade_api as tradeapi
import pandas as pd
from Utilies.utilies import dict_credential
import talib
from alpaca_trade_api import TimeFrame, TimeFrameUnit

API_KEY = dict_credential["API_KEY"]
API_SECRET = dict_credential["API_SECRET"]
APCA_API_BASE_URL = dict_credential["APCA_API_BASE_URL"]

# Creazione del client
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

# Simbolo dell'asset che si vuole analizzare
symbol = 'BTCUSD'

# Intervallo temporale del grafico
timeframe = '1D'

# Numero di giorni per la media mobile
period = 50

# Recupero dei dati storici dell'asset dal server Alpaca
historical_data = api.get_crypto_bars( symbol, timeframe= TimeFrame(1, TimeFrameUnit.Day),
                                start='2023-02-12', end='2023-02-26').df

# Calcolo della media mobile
sma = talib.SMA(historical_data['close'], timeperiod=period)

# Calcolo dell'RSI
rsi = talib.RSI(historical_data['close'], timeperiod=14)

# Conversione dei dati in un dataframe di Pandas per una facile visualizzazione
df = pd.DataFrame({'Close': historical_data['close'],
                   'SMA': sma,
                   'RSI': rsi})

# Stampa del dataframe
print(df)
