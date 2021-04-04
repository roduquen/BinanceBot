import numpy as np
from computing.ema import compute_ema

def compute_macd(prices, spans, signal_span):
  exp1 = compute_ema(prices, spans[0])
  exp2 = compute_ema(prices, spans[1])
  macd = exp1 - exp2
  signal = compute_ema(macd, signal_span)
  return macd, signal
