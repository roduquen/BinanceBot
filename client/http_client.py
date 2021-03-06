from binance_f import RequestClient
import numpy as np
import time
from binance_f.base.printobject import *
import threading

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
    self.mutex = threading.Lock()

  def get_candles(self, symbol, interval, amount):
    self.mutex.acquire()
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
    time.sleep(5)
    self.mutex.release()
    return array

  def market_order(self, side, symbol, quantity, reduce_only = False):
    self.mutex.acquire()
    result = self.client.post_order(
      symbol=symbol,
      side=side,
      ordertype="MARKET",
      quantity=quantity,
      reduceOnly=reduce_only
    )
    order_id = int(getattr(result, 'orderId'))
    time.sleep(5)
    self.mutex.release()
    return self.get_avg_price(symbol, order_id)

  def stop_market_order(self, side, symbol, stop_price):
    self.mutex.acquire()
    result = self.client.post_order(
      symbol=symbol,
      side=side,
      ordertype="STOP_MARKET",
      stopPrice=stop_price,
      closePosition=True
    )
    time.sleep(5)
    self.mutex.release()

  def get_avg_price(self, symbol, order_id):
    self.mutex.acquire()
    result = self.client.get_order(symbol=symbol, orderId=order_id)
    time.sleep(5)
    self.mutex.release()
    return float(getattr(result, 'avgPrice'))
