import numpy as np

def compute_ema(prices, size):
    alpha = 2 / (size + 1.0)
    alpha_rev = 1 - alpha
    n = prices.shape[0]
    pows = alpha_rev ** (np.arange(n + 1))
    scale_arr = 1 / pows[:-1]
    offset = prices[0] * pows[1:]
    pw0 = alpha * alpha_rev ** (n - 1)

    mult = prices * pw0 * scale_arr
    cumsums = mult.cumsum()
    ema = offset + cumsums * scale_arr[::-1]
    return ema
