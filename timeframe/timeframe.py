import numpy as np
import pandas as pd
import time
import threading
from binance_f.model import *
from binance_f.constant.test import *
from computing.rsi import compute_rsi
from computing.ema import compute_ema
from computing.macd import compute_macd
import mplfinance as mpf
import matplotlib.animation as animation
import matplotlib.pyplot as plt

INDEX = 110

class Timeframe:
  members = [
    'open',
    'high',
    'low',
    'close',
    'volume'
  ]
  candles = None
  ema = None
  rsi = None
  macd = None
  macd_signal = None

  def __init__(self, interval, symbol, http_client, clbk = None, clbk_args = ['candles']):
    self.interval = interval
    self.symbol = symbol
    self.clbk = clbk
    self.clbk_args = clbk_args
    self.set_candles(http_client)
    self.thread = threading.Thread(target=self.update_candles, args=(http_client,))
    self.thread.start()

  #############################
  #                           #
  #       CANDLES DATA        #
  #                           #
  #############################

  def next_candle_time(self):
    result = int((int(self.candles[INDEX, 0]) - round(time.time_ns() / 1000000) + int(self.interval["ms"]) + 1000) / 1000)
    if result < 0:
      result = 1
    return result

  def set_candles(self, client):
    self.candles = client.get_candles(self.symbol, self.interval["name"], INDEX + 1)
    self.set_indicators()
    self.launch_strategy()

  def update_candles(self, client):
    while True:
      time.sleep(15)
      new_candle = client.get_candles(self.symbol, self.interval["name"], 1)
      if self.candles[INDEX, 0] < new_candle[0, 0]:
        self.candles = np.append(np.delete(self.candles, 0, axis=0), [new_candle[0]], axis=0)
      else:
        self.candles[INDEX] = new_candle[0]
      self.set_indicators()
      self.launch_strategy()

  def get_candles(self):
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(self.candles, columns=columns)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Date')
    df.sort_values('Date', inplace=True)
    return df

  #############################
  #                           #
  #         STRATEGYS         #
  #                           #
  #############################

  def launch_strategy(self):
    if self.clbk is not None:
      array = []
      for member in self.clbk_args:
        if member == 'candles':
          array.append(self.candles)
        elif member == 'ema':
          array.append(self.ema)
        elif member == 'rsi':
          array.append(self.rsi)
        elif member == 'macd':
          array.append(self.macd)
        elif member == 'macd_signal':
          array.append(self.macd_signal)
      array.append(INDEX)
      self.clbk(array)

  #############################
  #                           #
  #        INDICATORS         #
  #                           #
  #############################

  def set_indicators(self):
    for member in self.clbk_args:
      if member == 'ema':
        self.set_ema()
      elif member == 'rsi':
        self.set_rsi()
      elif member == 'macd':
        self.set_macd()

  def set_macd(self):
    MACD_SIZE = 26
    SPANS = [12, MACD_SIZE]
    SIGNAL_SPAN = 9
    self.macd, self.macd_signal = compute_macd(self.candles[:, 4], SPANS, SIGNAL_SPAN)

  def set_rsi(self):
    RSI_SIZE = 14
    self.rsi = compute_rsi(self.candles[:, 4], RSI_SIZE)

  def set_ema(self):
    EMA_SIZE = 100
    self.ema = compute_ema(self.candles[:, 4], EMA_SIZE)

  #############################
  #                           #
  #         SHOW DATA         #
  #                           #
  #############################

  def show(self):
    candles = self.get_candles()
    ap = [
      mpf.make_addplot(
        self.rsi[:, 0],
        panel=2,
        type='line',
        ylabel='RSI',
      ),
      mpf.make_addplot(
        self.macd,
        panel=3,
        type='line',
        ylabel='MACD',
      ),
      mpf.make_addplot(
        self.macd_signal,
        panel=3,
        type='line',
      ),
      mpf.make_addplot(
        self.ema,
        panel=0,
        type='line',
        color='red'
      ),
    ]
    self.fig, self.axes = mpf.plot(
      candles,
      type='candle',
      title=self.symbol,
      style='binance',
      addplot=ap,
      mav=(3, 6, 9),
      volume=True,
      returnfig=True
    )
    self.ani = animation.FuncAnimation(self.fig,self.animate,interval=500)
    mpf.show()

  def animate(self, ival):
    candles = self.get_candles()
    for ax in self.axes:
        ax.clear()
        ax.grid(False)
    ap = [
      mpf.make_addplot(
        self.rsi[:, 0],
        panel=2,
        type='line',
        ylabel='RSI',
        ax=self.axes[4]
      ),
      mpf.make_addplot(
        self.macd,
        panel=3,
        type='line',
        ylabel='MACD',
        ax=self.axes[6],
        color="blue"
      ),
      mpf.make_addplot(
        self.macd_signal,
        panel=3,
        type='line',
        ax=self.axes[7],
        color="red"
      ),
      mpf.make_addplot(
        self.ema,
        panel=0,
        type='line',
        ax=self.axes[0],
        color='blue',
      ),
    ]
    self.axes[0].set_facecolor((0.2, 0.2, 0.2))
    self.axes[2].set_facecolor((0.2, 0.2, 0.2))
    self.axes[4].set_facecolor((0.2, 0.2, 0.2))
    self.axes[6].set_facecolor((0.2, 0.2, 0.2))
    self.axes[4].set_ylim([0, 100])
    self.axes[4].axline((0, 70), (1, 70), color='red', linewidth=1, dashes=(.5, .5))
    self.axes[4].axline((0, 30), (1, 30), color='green', linewidth=1, dashes=(.5, .5))
    self.axes[6].set_ylim([-100, 100])
    self.axes[6].axline((0, 0), (1, 0), color='black', linewidth=1, dashes=(.5, .5))
    mpf.plot(
      candles,
      type='candle',
      style='binance',
      mav=(3, 6, 9),
      addplot=ap,
      ax = self.axes[0],
      volume=self.axes[2]
    )


#
#  def update_candles(self, client):
#    client.connect(self.update_candles_callback, self.symbol.lower(), self.interval["name"])
#
#  def update_candles_callback(self, candle):
#    if self.candles[INDEX][0] == candle[0]:
#      self.candles[INDEX] = candle
#      self.set_rsi(False)
#    else:
#      self.candles = np.append(np.delete(self.candles, 0, axis=0), [candle], axis=0)
#      self.set_rsi(True)
