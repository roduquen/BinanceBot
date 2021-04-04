import numpy as np
import pandas as pd
import time
import threading
from timeframe.timeframe import Timeframe
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

class MACD_strategy:
  members = [
    'candles',
    'ema',
    'macd',
    'macd_signal'
  ]
  candles = None
  ema = None
  macd = None
  macd_signal = None
  in_trade = False
  avg_price = None
  stop_loss = None
  take_profit = None
  target_reached = False
  market_price = None
  profit = 0
  loss = 0

  def __init__(self, interval, symbol, min_quantity, portefolio, http_client, websocket_client):
    websocket_client.get_market(self.callback_websocket, symbol.lower())
    while self.market_price is None:
      time.sleep(1)
    self.http_client = http_client
    self.interval = interval
    self.symbol = symbol
    self.min_quantity = min_quantity
    self.portefolio = portefolio
    self.trade_value = portefolio / 25 # leverage
    self.timeframe = Timeframe(interval, symbol, http_client, self.launch_strategy, self.members)

  def launch_strategy(self, values):
    uptrend = None
    downtrend = None
    signal_up = None
    macd_pos = None
    macd_neg = None
    if self.candles is not None:
      uptrend, downtrend, signal_up, macd_pos, macd_neg = self.trend_values()
    self.candles = values[0]
    self.ema = values[1]
    self.macd = values[2]
    self.macd_signal = values[3]
    self.index = values[4]
    if uptrend is not None:
      uptrend2, downtrend2, signal_up2, macd_pos2, macd_neg2 = self.trend_values()
      if (uptrend is True and uptrend2 is True
        and signal_up is True and signal_up2 is False
        and macd_neg is True and macd_neg2 is True):
        self.enter_long()
      elif (downtrend is True and downtrend2 is True
        and signal_down is True and signal_down2 is False
        and macd_pos is True and macd_pos2 is True):
        self.enter_short()

  def callback_websocket(self, market):
    self.market_price = market
    if self.in_trade is True:
      if self.position == "LONG":
        if market <= self.stop_loss:
          self.exit_position()
          self.loss += 1
          print("TOTAL LOSS: ", self.loss, "\n", "TOTAL GAIN: ", self.profit)
        if self.target_reached is True and market <= self.take_profit:
          self.exit_position()
          self.profit += 1
          print("TOTAL LOSS: ", self.loss, "\n", "TOTAL GAIN: ", self.profit)
        elif self.target_reached is False and market >= self.take_profit:
          self.start_grinding()

  def exit_position(self):
    self.in_trade = False
    side = "SELL"
    if self.position == "SHORT":
      side = "BUY"
    self.http_client.market_order(
      side,
      self.symbol,
      self.quantity,
      true
    )
    self.position = None
    self.quantity = None
    self.avg_price = None
    self.stop_loss = None
    self.take_profit = None

  def start_grinding(self):
    def callback():
      time.sleep(30)
      if ((self.position == "LONG" and self.market_value >= self.take_profit)
        or (position == "SHORT" and self.market_value <= self.take_profit)):
        while self.in_trade is True:
          self.target_reached = True
          new_take_profit = (self.take_profit + self.market_price) / 2
          if self.position == "LONG" and new_take_profit > self.take_profit:
            self.take_profit = new_take_profit
          if self.position == "SHORT" and new_take_profit < self.take_profit:
            self.take_profit = new_take_profit
          time.sleep(60)
      return
    self.thread = threading.Thread(target=callback)
    self.thread.start()

  def trend_values(self):
    uptrend = self.candles[self.index, 3] - self.ema[self.index] > 0
    downtrend = self.candles[self.index, 2] - self.ema[self.index] < 0
    signal_up = self.macd_signal[self.index] > self.macd[self.index]
    macd_pos = self.macd[self.index] > 0.05
    macd_neg = self.macd[self.index] < -0.05
    return uptrend, downtrend, signal_up, macd_pos, macd_neg

  def compute_quantity(self):
    price = self.market_price
    min_quantity = self.min_quantity
    value = self.trade_value * 25 # leverage
    quantity = value / price
    quantity = quantity - quantity % min_quantity
    return quantity


  def enter_long(self):
    if self.in_trade is True:
      self.exit_position()
    side = "BUY"
    symbol = self.symbol
    quantity = self.compute_quantity()
    self.avg_price = self.http_client.market_order(
      side,
      symbol,
      quantity
    )
    self.quantity = quantity
    self.stop_loss = self.avg_price * 0.99
    self.take_profit = self.avg_price * 1.0125
    self.position = "LONG"
    self.in_trade = True

  def enter_short(self):
    if self.in_trade is True:
      self.exit_position()
    side = "SELL"
    symbol = self.symbol
    quantity = self.compute_quantity()
    self.avg_price = self.http_client.market_order(
      side,
      symbol,
      quantity
    )
    self.quantity = quantity
    self.stop_loss = self.avg_price * 1.01
    self.take_profit = self.avg_price * 0,9875
    self.position = "SHORT"
    self.in_trade = True
