import numpy as np
from binance_f import SubscriptionClient
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.base.printobject import *

class WebSocketClient:
  members = [
    'open',
    'high',
    'low',
    'close',
    'volume'
  ]
  def __init__(self, api_key_id, api_secret_key):
    self.client = SubscriptionClient(api_key=api_key_id, secret_key=api_secret_key)

  def get_candles(self, clbk, symbol, interval):
    def callback(data_type: 'SubscribeMessageType', event: 'any'):
      if data_type == SubscribeMessageType.PAYLOAD:
        candle = np.array([ int(getattr(event.data, 'startTime')) ])
        for member in self.members:
          candle = np.append(candle, [ float(getattr(event.data, member)) ])
        clbk(candle)
    self.client.subscribe_candlestick_event(
      symbol,
      interval,
      callback,
      self.error
    )

  def get_market(self, clbk, symbol):
    def callback(data_type: 'SubscribeMessageType', event: 'any'):
      if data_type == SubscribeMessageType.PAYLOAD:
        clbk(float(getattr(event, "markPrice")))
    self.client.subscribe_mark_price_event(
      symbol,
      callback,
      self.error
    )

  def error(self, e: 'BinanceApiException'):
    print(e.error_code + e.error_message)
    exit()

