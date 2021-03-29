import numpy as np
import pandas as pd
from binance_f.model import *
from binance_f.constant.test import *
from computing.rsi import compute_rsi
import mplfinance as mpf
import matplotlib.animation as animation

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

  def __init__(self, interval, symbol, http_client, websocket_client):
    self.interval = interval
    self.symbol = symbol
    self.set_candles(http_client)
    self.update_candles(websocket_client)
    self.set_rsi(True)

  def set_candles(self, client):
    self.candles = client.get_candles(self.symbol, self.interval, INDEX + 1)

  def update_candles(self, client):
    client.connect(self.update_candles_callback, self.symbol.lower(), self.interval)

  def update_candles_callback(self, candle):
    if self.candles[INDEX][0] == candle[0]:
      self.candles[INDEX] = candle
      self.set_rsi(False)
    else:
      self.candles = np.append(np.delete(self.candles, 0, axis=0), [candle], axis=0)
      self.set_rsi(True)

  def get_candles(self):
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI14_1', 'RSI14_2']
    array = np.insert(self.candles, 6, self.rsi[:, 0], axis=1)
    array = np.insert(array, 7, self.rsi[:, 1], axis=1)
    df = pd.DataFrame(array, columns=columns)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Date')
    df.sort_values('Date', inplace=True)
    return df

  def set_rsi(self, new):
    if self.rsi is None:
      self.rsi = compute_rsi(self.candles[:, 4], 14)
    else:
      new_rsi = compute_rsi(self.candles[-15:,  4], 14)[14]
      if new is True:
        self.rsi = np.append(np.delete(self.rsi, 0, axis=0), [new_rsi], axis=0)
      else:
        self.rsi[INDEX] = new_rsi

  def show(self):
    show_graph = True
    ap = mpf.make_addplot(
      self.rsi[:, 0],
      panel=2,
      type='line',
      ylabel='RSI',
    )
    self.fig, self.axes = mpf.plot(
      self.get_candles(),
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
    for ax in self.axes:
        ax.clear()
    ap = mpf.make_addplot(
      self.rsi[:, 0],
      panel=2,
      type='line',
      ylabel='RSI',
      ax=self.axes[4]
    )
    self.axes[4].set_ylim([0, 100])
    self.axes[4].axline((0, 70), (1, 70), color='red', linewidth=1, dashes=(.5, .5))
    self.axes[4].axline((0, 30), (1, 30), color='green', linewidth=1, dashes=(.5, .5))
    mpf.plot(
      self.get_candles(),
      type='candle',
      style='binance',
      mav=(3, 6, 9),
      addplot=ap,
      ax = self.axes[0],
      volume=self.axes[2]
    )

