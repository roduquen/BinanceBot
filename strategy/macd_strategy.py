import numpy as np
import pandas as pd
import time
from datetime import datetime
import threading
from timeframe.timeframe import Timeframe
from binance_f.constant.test import *
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
    self.http_client = http_client
    self.interval = interval
    self.symbol = symbol
    self.min_quantity = min_quantity
    self.portefolio = portefolio
    self.trade_value = portefolio / 25 # leverage
    self.timeframe = Timeframe(interval, symbol, http_client, websocket_client, self.launch_strategy, self.members)

  def launch_strategy(self, values):
    uptrend = None
    downtrend = None
    signal_up = None
    macd_pos = None
    macd_neg = None
    opened = False
    if self.candles is not None:
      opened = True
    self.candles = values[0]
    self.ema = values[1]
    self.macd = values[2]
    self.macd_signal = values[3]
    self.index = values[4]
    self.market_price = self.candles[self.index, 4]
    if opened is True:
      uptrend, downtrend, signal_up, macd_pos, macd_neg, l, s = self.trend_values(True, -1)
      uptrend2, downtrend2, signal_up2, macd_pos2, macd_neg2, possible_long, possible_short = self.trend_values()
      if possible_long:
        if uptrend2:
          if signal_up:
            if not signal_up2:
              if macd_neg2:
                self.enter_long()
      elif possible_short:
        if downtrend2:
          if not signal_up:
            if signal_up2:
              if macd_pos2:
                self.enter_short()
      if self.in_trade is True:
        if self.target_reached is True:
          new_take_profit = (self.ema[self.index - 1] + self.candles[self.index - 1, 4]) / 2
          if self.position == "LONG":
            if new_take_profit > self.take_profit:
              self.take_profit = new_take_profit
          else:
            if new_take_profit < self.take_profit:
              self.take_profit = new_take_profit
        self.strategy_launched(self.candles[self.index, 4])

  def strategy_launched(self, market):
    self.market_price = market
    if self.in_trade is True:
      if self.position == "LONG":
        if market <= self.stop_loss:
          self.exit_position()
          self.loss += 1
          print(datetime.now(), " : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        if self.target_reached is True and market <= self.take_profit:
          self.exit_position()
          self.profit += 1
          print(datetime.now(), " : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        elif self.target_reached is False and market >= self.take_profit:
          self.start_grinding()
      else:
        if market >= self.stop_loss:
          self.exit_position()
          self.loss += 1
          print(datetime.now(), " : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        if self.target_reached is True and market >= self.take_profit:
          self.exit_position()
          self.profit += 1
          print(datetime.now(), " : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        elif self.target_reached is False and market <= self.take_profit:
          self.start_grinding()

  def exit_position(self):
    self.in_trade = False
    side = "SELL"
    if self.position == "SHORT":
      side = "BUY"
    result = self.http_client.market_order(
      side,
      self.symbol,
      self.quantity,
      true
    )
    print(datetime.now(), " : ", self.symbol, " : ", self.position, " : Opened at => ", self.avg_price, " Closed at => ", result)
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
        self.target_reached = True
      return
    self.thread = threading.Thread(target=callback)
    self.thread.start()

  def trend_values(self, first = False, padding = 0):
    index = self.index + padding
    i = index - 11
    uptrend = True
    while uptrend and i < index:
      uptrend = (self.candles[i, 3] + self.candles[i, 2]) / 2 > self.ema[i]
      i += 1
    i = index - 11
    downtrend = True
    while downtrend and i < index:
      downtrend = (self.candles[i, 3] + self.candles[i, 2]) < self.ema[i]
      i += 1
    signal_up = self.macd_signal[index] > self.macd[index]
    macd_pos = self.macd[index] >= 0
    macd_neg = self.macd[index] < 0
    possible_long = self.candles[index, 4] >= self.ema[index] * 1.0125
    possible_short = self.candels[index, 4] <= self.ema[index] * 0.9875
    return uptrend, downtrend, signal_up, macd_pos, macd_neg, possible_long, possible_short

  def compute_quantity(self):
    price = self.market_price
    min_quantity = self.min_quantity
    value = self.trade_value * 25 # leverage
    quantity = value / price
    quantity = quantity - quantity % min_quantity
    if min_quantity == 1:
      quantity = round(quantity)
    elif min_quantity == 0.1:
      quantity = round(quantity, 1)
    elif min_quantity == 0.01:
      quantity = round(quantity, 2)
    elif min_quantity == 0.001:
      quantity = round(quantity, 3)
    return quantity


  def enter_long(self):
    if self.in_trade is False:
      side = "BUY"
      symbol = self.symbol
      quantity = self.compute_quantity()
      self.avg_price = self.http_client.market_order(
        side,
        symbol,
        quantity
      )
      print(datetime.now(), " : Enter Long => ", self.avg_price)
      self.quantity = quantity
      self.stop_loss = self.avg_price * 0.99
      self.take_profit = self.avg_price * 1.0125
      self.position = "LONG"
      self.in_trade = True

  def enter_short(self):
    if self.in_trade is False:
      side = "SELL"
      symbol = self.symbol
      quantity = self.compute_quantity()
      self.avg_price = self.http_client.market_order(
        side,
        symbol,
        quantity
      )
      print(datetime.now(), " : Enter Short => ", self.avg_price)
      self.quantity = quantity
      self.stop_loss = self.avg_price * 1.01
      self.take_profit = self.avg_price * 0.9875
      self.position = "SHORT"
      self.in_trade = True
