import numpy as np
import pandas as pd
import time
import threading
from binance_f.model import *
from binance_f.constant.test import *
from computing.rsi import compute_rsi
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
  rsi = None
  show_graph = False
  macd = None
  signal = None

  def __init__(self, interval, symbol, http_client):
    self.interval = interval
    self.symbol = symbol
    self.set_candles(http_client)
    thread = threading.Thread(target=self.update_candles, args=(http_client,))
    thread.start()

  def next_candle_time(self, client):
    result = int((int(self.candles[INDEX][0]) - round(time.time_ns() / 1000000) + int(self.interval["ms"]) + 1000) / 1000)
    if result <= 0:
      result = self.interval["ms"] / 1000
    return result

  def update_candles(self, client):
    while True:
      time.sleep(self.next_candle_time(client))
      new_candle = client.get_candles(self.symbol, self.interval["name"], 2)
      if self.candles[INDEX, 0] < new_candle[0][0]:
        self.candles = np.append(np.delete(self.candles, 0, axis=0), [new_candle[0]], axis=0)
      if self.candles[INDEX, 0] < new_candle[1][0]:
        self.candles = np.append(np.delete(self.candles, 0, axis=0), [new_candle[1]], axis=0)
        self.set_rsi()

  def set_candles(self, client):
    self.candles = client.get_candles(self.symbol, self.interval["name"], INDEX + 1)
    self.set_rsi()
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

  def get_candles(self):
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI14_1', 'RSI14_2']
    array = np.insert(self.candles, 6, self.rsi[:, 0], axis=1)
    array = np.insert(array, 7, self.rsi[:, 1], axis=1)
    df = pd.DataFrame(array, columns=columns)
    self.compute_macd(df)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Date')
    df.sort_values('Date', inplace=True)
    return df

  def compute_macd(self, df):
    exp1 = df.Close.ewm(span=12, adjust=False).mean()
    exp2 = df.Close.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    self.macd = macd.to_numpy()
    signal = macd.ewm(span=9, adjust=False).mean()
    self.signal = signal.to_numpy()

  def set_rsi(self):
    RSI_SIZE = 14
    if self.rsi is None:
      self.rsi = compute_rsi(self.candles[:, 4], RSI_SIZE)
    else:
      new_rsi = compute_rsi(self.candles[-(RSI_SIZE + 1):,  4], RSI_SIZE)[RSI_SIZE]
      self.rsi = np.append(np.delete(self.rsi, 0, axis=0), [new_rsi], axis=0)

  def show(self):
    show_graph = True
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
        self.signal,
        panel=3,
        type='line',
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
    ap = mpf.make_addplot(
      self.rsi[:, 0],
      panel=2,
      type='line',
      ylabel='RSI',
    )
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
        self.signal,
        panel=3,
        type='line',
        ax=self.axes[7],
        color="red"
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
    mpf.plot(
      candles,
      type='candle',
      style='binance',
      mav=(3, 6, 9),
      addplot=ap,
      ax = self.axes[0],
      volume=self.axes[2]
    )
