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

INDEX = 249

class Array:
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

  def __init__(self, interval, symbol, http_client):
    self.interval = interval
    self.symbol = symbol
    self.set_candles(http_client)
    thread = threading.Thread(target=self.update_candles, args=(http_client,))
    thread.start()

  #############################
  #                           #
  #       CANDLES DATA        #
  #                           #
  #############################

  def next_candle_time(self, client):
    result = int((int(self.candles[INDEX][0]) - round(time.time_ns() / 1000000) + int(self.interval["ms"]) + 1000) / 1000)
    if result <= 0:
      result = self.interval["ms"] / 1000
    return result

  def set_candles(self, client):
    self.candles = client.get_candles(self.symbol, self.interval["name"], INDEX + 1)
    self.set_indicators()

  def update_candles(self, client):
    while True:
      time.sleep(self.next_candle_time(client))
      new_candle = client.get_candles(self.symbol, self.interval["name"], 2)
      if self.candles[INDEX, 0] < new_candle[0][0]:
        self.candles = np.append(np.delete(self.candles, 0, axis=0), [new_candle[0]], axis=0)
      if self.candles[INDEX, 0] < new_candle[1][0]:
        self.candles = np.append(np.delete(self.candles, 0, axis=0), [new_candle[1]], axis=0)
        self.set_indicators()
        self.get_candles()

  def get_candles(self):
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI14_1', 'RSI14_2']
    array = np.insert(self.candles, 6, self.rsi[:, 0], axis=1)
    array = np.insert(array, 7, self.rsi[:, 1], axis=1)
    df = pd.DataFrame(array, columns=columns)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Date')
    df.sort_values('Date', inplace=True)
    return df

  #############################
  #                           #
  #        INDICATORS         #
  #                           #
  #############################

  def set_indicators(self):
    self.set_rsi()
    self.set_macd()
    self.set_ema()

  def set_macd(self):
    MACD_SIZE = 26
    SPANS = [12, MACD_SIZE]
    SIGNAL_SPAN = 9
    if self.macd is None:
      self.macd, self.macd_signal = compute_macd(self.candles[:, 4], SPANS, SIGNAL_SPAN)
    else:
      new_macd, new_signal = compute_macd(self.candles[-(MACD_SIZE + 1):,  4], SPANS, SIGNAL_SPAN)
      new_macd = new_macd[MACD_SIZE]
      new_signal = new_signal[MACD_SIZE]
      self.macd = np.append(np.delete(self.macd, 0, axis=0), [new_macd], axis=0)
      self.macd_signal = np.append(np.delete(self.macd_signal, 0, axis=0), [new_signal], axis=0)


  def set_rsi(self):
    RSI_SIZE = 14
    if self.rsi is None:
      self.rsi = compute_rsi(self.candles[:, 4], RSI_SIZE)
    else:
      new_rsi = compute_rsi(self.candles[-(RSI_SIZE + 1):,  4], RSI_SIZE)[RSI_SIZE]
      self.rsi = np.append(np.delete(self.rsi, 0, axis=0), [new_rsi], axis=0)

  def set_ema(self):
    EMA_SIZE = 100
    if self.ema is None:
      self.ema = compute_ema(self.candles[:, 4], EMA_SIZE)
    else:
      new_ema = compute_ema(self.candles[-(EMA_SIZE + 1):,  4], EMA_SIZE)[EMA_SIZE]
      self.ema = np.append(np.delete(self.ema, 0, axis=0), [new_ema], axis=0)

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
    self.ani = animation.FuncAnimation(self.fig,self.animate,interval=50)
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
    self.axes[6].set_ylim([-1, 1])
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
