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
  ema_50 = None
  macd = None
  macd_signal = None
  in_trade = False
  avg_price = None
  stop_loss = None
  take_profit = None
  target_reached = False
  market_price = None
  thread = None
  profit = 0
  loss = 0
  wait = False
  last_take_update = 0
  wait_time = 0

  def __init__(self, interval, symbol, min_quantity, portefolio, http_client, websocket_client):
    self.http_client = http_client
    self.interval = interval
    self.symbol = symbol
    self.min_quantity = min_quantity
    self.portefolio = portefolio
    self.trade_value = portefolio / 25 # leverage
    self.timeframe = Timeframe(interval, symbol, http_client, websocket_client, self.launch_strategy, self.members)

  def launch_strategy(self, values):
    if self.wait is True:
      if self.wait_time + 36000000 < time.time_ns() / 1000000:
        self.wait = False
    else:
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
      self.ema_50 = values[2]
      self.macd = values[3]
      self.macd_signal = values[4]
      self.index = values[5]
      self.market_price = self.candles[self.index, 4]
      if opened is True:
        uptrend, downtrend, signal_up, macd_pos, macd_neg = self.trend_values(True, -1)
        uptrend2, downtrend2, signal_up2, macd_pos2, macd_neg2 = self.trend_values()
        if uptrend2:
          if signal_up:
            if not signal_up2:
              if macd_neg2:
                self.enter_long()
        elif downtrend2:
          if not signal_up:
            if signal_up2:
              if macd_pos2:
                self.enter_short()
        if self.in_trade is True:
          if self.target_reached is True:
            if time.time_ns() / 1000000 - self.interval["ms"] / 5 > self.last_take_update:
              self.last_take_update = time.time_ns() / 1000000
              new_take_profit = self.candles[self.index, 2] * 0.2 + self.candles[self.index, 3] * 0.2 + self.take_profit * 0.4 + self.ema_50[self.index] * 0.2
              if self.position == "LONG":
                if new_take_profit > self.take_profit:
                  self.take_profit = new_take_profit
              elif self.position == "SHORT":
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
        if self.target_reached is True:
          if market <= self.take_profit:
            self.exit_position()
            self.profit += 1
            print(datetime.now(), " : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        elif self.target_reached is False:
          if market >= self.take_profit:
            self.start_grinding()
      elif self.position == "SHORT":
        if market >= self.stop_loss:
          self.exit_position()
          self.loss += 1
          print(datetime.now(), " : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        if self.target_reached is True:
          if market >= self.take_profit:
            self.exit_position()
            self.profit += 1
            print(datetime.now(), " : ", self.symbol, ": TOTAL LOSS => ", self.loss, " TOTAL GAIN => ", self.profit)
        elif self.target_reached is False:
          if market <= self.take_profit:
            self.start_grinding()

  def exit_position(self):
    self.wait_time = time.time_ns() / 1000000
    self.wait = True
    side = "SELL"
    if self.position == "SHORT":
      side = "BUY"
    result = self.http_client.market_order(
      side,
      self.symbol,
      self.quantity,
      True
    )
    print(datetime.now(), " : ", self.symbol, " : ", self.position, " : Opened at => ", self.avg_price, " Closed at => ", result)
    self.position = None
    self.quantity = None
    self.avg_price = None
    self.stop_loss = None
    self.take_profit = None
    self.target_reached = False
    self.in_trade = False

  def start_grinding(self):
    def callback():
      time.sleep(30)
      if self.position == "LONG":
        if self.market_price >= self.take_profit:
          self.last_take_update = time.time_ns() / 1000000
          self.target_reached = True
          return
      elif self.position == "SHORT":
        if self.market_price <= self.take_profit:
          self.last_take_update = time.time_ns() / 1000000
          self.target_reached = True
          return
    if self.thread is None:
      self.thread = threading.Thread(target=callback)
      self.thread.start()
      self.thread.join()
      self.thread = None

  def trend_values(self, first = False, padding = 0):
    index = self.index + padding
    uptrend = self.candles[index, 3] > self.ema[index]
    if uptrend:
      count = 0
      i = index - 25
      max_value = 0
      while i < index:
        if max_value < self.candles[i, 4]:
          max_value = self.candles[i, 4]
        if self.candles[i, 4] > self.ema[i]:
          count += 1
        i += 1
      if max_value > self.candles[i, 4] * 1.015:
        if count > 18:
          uptrend = True
        else:
          uptrend = False
      else:
        uptrend = False
    downtrend = self.candles[index, 2] < self.ema[index]
    if downtrend:
      i = index - 25
      count = 0
      min_value = 1000000
      while i < index:
        if min_value > self.candles[i, 4]:
          min_value = self.candles[i, 4]
        if self.candles[i, 4] < self.ema[i]:
          count += 1
        i += 1
      if min_value < self.candles[i, 4] * 0.985:
        if count > 18:
          downtrend = True
        else:
          downtrend = False
      else:
        downtrend = False
    signal_up = self.macd_signal[index] > self.macd[index]
    macd_pos = self.macd[index] >= 0
    macd_neg = self.macd[index] < 0
    return uptrend, downtrend, signal_up, macd_pos, macd_neg

  def compute_quantity(self):
    price = self.market_price
    min_quantity = self.min_quantity
    value = self.trade_value * 25 # leverage
    quantity = value / price
    quantity = quantity - quantity % min_quantity
    quantity /= min_quantity
    quantity = round(quantity)
    if min_quantity == 0.1:
      quantity = "{:0.0{}f}".format(quantity / 10, 1)
    elif min_quantity == 0.01:
      quantity = "{:0.0{}f}".format(quantity / 100, 2)
    elif min_quantity == 0.001:
      quantity = "{:0.0{}f}".format(quantity / 1000, 3)
    return quantity


  def enter_long(self):
    if self.in_trade is False:
      if self.wait is False:
        side = "BUY"
        symbol = self.symbol
        quantity = self.compute_quantity()
        self.in_trade = True
        self.avg_price = self.http_client.market_order(
          side,
          symbol,
          quantity
        )
        print(datetime.now(), " : Enter Long => ", self.avg_price)
        self.quantity = quantity
        self.stop_loss = self.avg_price * 0.99
        self.take_profit = self.avg_price * 1.015
        self.position = "LONG"

  def enter_short(self):
    if self.in_trade is False:
      if self.wait is False:
        side = "SELL"
        symbol = self.symbol
        quantity = self.compute_quantity()
        self.in_trade = True
        self.avg_price = self.http_client.market_order(
          side,
          symbol,
          quantity
        )
        print(datetime.now(), " : Enter Short => ", self.avg_price)
        self.quantity = quantity
        self.stop_loss = self.avg_price * 1.01
        self.take_profit = self.avg_price * 0.985
        self.position = "SHORT"
