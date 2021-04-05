import numpy as np
import pandas as pd
import time
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
    open = False
    if self.candles is not None:
      open = True
    self.candles = values[0]
    self.ema = values[1]
    self.macd = values[2]
    self.macd_signal = values[3]
    self.index = values[4]
    if open is True:
      uptrend, downtrend, signal_up, macd_pos, macd_neg = self.trend_values(True, -1)
      uptrend2, downtrend2, signal_up2, macd_pos2, macd_neg2 = self.trend_values()
      if (uptrend2 is True
        and signal_up is True and signal_up2 is False
        and macd_neg2 is True):
        print(
          "MAGESSTY : ",
          self.symbol,
          " UPTREND = ",
          uptrend,
          " DOWNTREND = ",
          downtrend,
          " SIGNAL UP = ",
          signal_up,
          " MACD_POS = ",
          macd_pos,
          " MACD_NEG = ",
          macd_neg
        )
        print(
          "MAGESSTY : ",
          self.symbol,
          " UPTREND2 = ",
          uptrend2,
          " DOWNTREND2 = ",
          downtrend2,
          " SIGNAL UP2 = ",
          signal_up2,
          " MACD_POS2 = ",
          macd_pos2,
          " MACD_NEG2 = ",
          macd_neg2
        )
        self.enter_long()
      elif (downtrend2 is True
        and signal_up is False and signal_up2 is True
        and macd_pos2 is True):
        print(
          "MAGESSTY : ",
          self.symbol,
          " UPTREND = ",
          uptrend,
          " DOWNTREND = ",
          downtrend,
          " SIGNAL UP = ",
          signal_up,
          " MACD_POS = ",
          macd_pos,
          " MACD_NEG = ",
          macd_neg
        )
        print(
          "MAGESSTY : ",
          self.symbol,
          " UPTREND2 = ",
          uptrend2,
          " DOWNTREND2 = ",
          downtrend2,
          " SIGNAL UP2 = ",
          signal_up2,
          " MACD_POS2 = ",
          macd_pos2,
          " MACD_NEG2 = ",
          macd_neg2
        )
        self.enter_short()
      if self.in_trade is True:
        if self.target_reached is True:
          self.take_profit = (self.take_profit + self.candles[self.index, 4]) / 2
        self.strategy_launched(self.candles[self.index, 4])

  def strategy_launched(self, market):
    self.market_price = market
    if self.in_trade is True:
      if self.position == "LONG":
        if market <= self.stop_loss:
          self.exit_position()
          self.loss += 1
          print("MAGESSTY : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        if self.target_reached is True and market <= self.take_profit:
          self.exit_position()
          self.profit += 1
          print("MAGESSTY : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        elif self.target_reached is False and market >= self.take_profit:
          self.start_grinding()
      else:
        if market >= self.stop_loss:
          self.exit_position()
          self.loss += 1
          print("MAGESSTY : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        if self.target_reached is True and market >= self.take_profit:
          self.exit_position()
          self.profit += 1
          print("MAGESSTY : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        elif self.target_reached is False and market <= self.take_profit:
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
        self.target_reached = True
      return
    self.thread = threading.Thread(target=callback)
    self.thread.start()

  def trend_values(self, first = False, padding = 0):
    index = self.index + padding
    uptrend = self.candles[index, 3] > self.ema[index]
    downtrend = self.candles[index, 2] < self.ema[index]
    signal_up = self.macd_signal[index] > self.macd[index]
    macd_pos = self.macd[index] > 0.05
    macd_neg = self.macd[index] < -0.05
    return uptrend, downtrend, signal_up, macd_pos, macd_neg

  def compute_quantity(self):
    price = self.market_price
    min_quantity = self.min_quantity
    value = self.trade_value * 25 # leverage
    quantity = value / price
    quantity = quantity - quantity % min_quantity
    return quantity


  def enter_long(self):
    if self.in_trade is True and self.position == "SHORT":
      self.exit_position()
    if self.in_trade is False:
      side = "BUY"
      symbol = self.symbol
      quantity = self.compute_quantity()
      self.avg_price = self.http_client.market_order(
        side,
        symbol,
        quantity
      )
      print("MAGESSTY : Enter Long => ", self.avg_price)
      self.quantity = quantity
      self.stop_loss = self.avg_price * 0.99
      self.take_profit = self.avg_price * 1.0125
      self.position = "LONG"
      self.in_trade = True

  def enter_short(self):
    if self.in_trade is True and self.position == "LONG":
      self.exit_position()
    if self.in_trade is False:
      side = "SELL"
      symbol = self.symbol
      quantity = self.compute_quantity()
      self.avg_price = self.http_client.market_order(
        side,
        symbol,
        quantity
      )
      print("MAGESSTY : Enter Short => ", self.avg_price)
      self.quantity = quantity
      self.stop_loss = self.avg_price * 1.01
      self.take_profit = self.avg_price * 0,9875
      self.position = "SHORT"
      self.in_trade = True
