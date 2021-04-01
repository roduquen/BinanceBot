from binance_f import RequestClient
import numpy as np

class HTTPClient:
  members = [
    'open',
    'high',
    'low',
    'close',
    'volume',
  ]

  def __init__(self, api_key_id, api_secret_key):
    self.client = RequestClient(api_key=api_key_id, secret_key=api_secret_key)

  def get_candles(self, symbol, interval, amount):
    candles = self.client.get_candlestick_data(
      symbol=symbol,
      interval=interval,
      limit=amount
    )
    array = None
    for candle in candles:
      candle_x = np.array([ int(getattr(candle, 'openTime')) ])
      for member in self.members:
        candle_x = np.append(candle_x, [float(getattr(candle, member))])
      if array is None:
        array = np.array([candle_x])
      else:
        array = np.append(array, [candle_x], axis=0)
    return array
