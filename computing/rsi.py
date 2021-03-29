import numpy as np

def rsi_0_100(prices, interval):
  upPrices = np.array([])
  downPrices = np.array([])
  i = 0
  while i < len(prices):
    if i == 0:
      upPrices = np.append(upPrices, [0])
      downPrices = np.append(downPrices, [0])
    else:
      price_diff = prices[i] - prices[i - 1]
      if price_diff > 0:
        upPrices = np.append(upPrices, [price_diff])
        downPrices = np.append(downPrices, [0])
      else:
        downPrices = np.append(downPrices, [price_diff])
        upPrices = np.append(upPrices, [0])
    i += 1


  avg_gain = np.array([])
  avg_loss = np.array([])
  x = 0
  while x < len(upPrices):
    if x < interval:
      avg_gain = np.append(avg_gain, [0])
      avg_loss = np.append(avg_loss, [0])
    else:
      sumGain = 0
      sumLoss = 0
      y = x - interval
      while y <= x:
        sumGain += upPrices[y]
        sumLoss += downPrices[y]
        y += 1
      avg_gain = np.append(avg_gain, [sumGain / 14])
      avg_loss = np.append(avg_loss, [abs(sumLoss / 14)])
    x += 1


  RS = np.array([])
  RSI = np.array([])
  p = 0
  while p < len(prices):
    if p < interval:
      RS = np.append(RS, [0])
      RSI = np.append(RSI, [0])
    else:
      RSvalue = avg_gain[p] / avg_loss[p]
      RS = np.append(RS, [RSvalue])
      RSI = np.append(RSI, [100 - (100 / (1 + RSvalue))])
    p+=1
  return RSI

def rsi_minus_1_1_from_rsi(RSI):
  i = 0
  RSI_minus_1_1 = np.array([])
  while i < len(RSI):
    RSI_minus_1_1 = np.append(RSI_minus_1_1, [RSI[i] / 50 - 1])
    i += 1
  return RSI_minus_1_1

def rsi_net(RSI):
  i = 1
  X = np.array([])
  Y = np.array([])
  while i < len(RSI):
    X = np.append(X, [RSI[i - 1]])
    Y = np.append(Y, [-i])
    i += 1

def compute_rsi(prices, interval):
  RSI_0_100 = rsi_0_100(prices, interval)
  RSI_minus_1_1 = rsi_minus_1_1_from_rsi(RSI_0_100)
  array = np.array([RSI_0_100, RSI_minus_1_1]).T;
  return array
