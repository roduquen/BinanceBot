from client.websocket_client import WebSocketClient
from client.http_client import HTTPClient
from strategy.macd_strategy import MACD_strategy
from binance_keys import *
import time
import sys

http_client = HTTPClient(api_key_id, secret_key)
websocket_client = WebSocketClient(api_key_id, secret_key)

for pool in sys.argv:
  if pool == "1":
    btc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BTCUSDT", 0.001, 550, http_client, websocket_client)
    bch = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BCHUSDT", 0.001, 550, http_client, websocket_client)
    eth = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ETHUSDT", 0.001, 550, http_client, websocket_client)
    etc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ETCUSDT", 0.01, 550, http_client, websocket_client)
    ltc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LTCUSDT", 0.001, 550, http_client, websocket_client)
    xrp = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XRPUSDT", 0.1, 550, http_client, websocket_client)
    eos = MACD_strategy({"name" : "30m", "ms" : 1800000}, "EOSUSDT", 0.1, 550, http_client, websocket_client)
    ada = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ADAUSDT", 1, 550, http_client, websocket_client)
    avax = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AVAXUSDT", 1, 550, http_client, websocket_client)
    xlm = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XLMUSDT", 1, 550, http_client, websocket_client)
  elif pool == "2":
    trx = MACD_strategy({"name" : "30m", "ms" : 1800000}, "TRXUSDT", 1, 550, http_client, websocket_client)
    link = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LINKUSDT", 0.01, 550, http_client, websocket_client)
    bnb = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BNBUSDT", 0.01, 550, http_client, websocket_client)
    xmr = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XMRUSDT", 0.001, 550, http_client, websocket_client)
    dash = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DASHUSDT", 0.001, 550, http_client, websocket_client)
    zec = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ZECUSDT", 0.001, 550, http_client, websocket_client)
    xtz = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XTZUSDT", 0.1, 550, http_client, websocket_client)
    atom = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ATOMUSDT", 0.01, 550, http_client, websocket_client)
    ont = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ONTUSDT", 0.1, 550, http_client, websocket_client)
    enj = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ENJUSDT", 1, 550, http_client, websocket_client)
  elif pool == "3":
    axs = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AXSUSDT", 1, 550, http_client, websocket_client)
    chz = MACD_strategy({"name" : "30m", "ms" : 1800000}, "CHZUSDT", 1, 550, http_client, websocket_client)
    dot = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DOTUSDT", 0.1, 550, http_client, websocket_client)
    inch = MACD_strategy({"name" : "30m", "ms" : 1800000}, "1INCHUSDT", 1, 550, http_client, websocket_client)
    uni = MACD_strategy({"name" : "30m", "ms" : 1800000}, "UNIUSDT", 1, 550, http_client, websocket_client)
    sushi = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SUSHIUSDT", 1, 550, http_client, websocket_client)
    sxp = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SXPUSDT", 0.1, 550, http_client, websocket_client)
    iota = MACD_strategy({"name" : "30m", "ms" : 1800000}, "IOTAUSDT", 0.1, 550, http_client, websocket_client)
    vet = MACD_strategy({"name" : "30m", "ms" : 1800000}, "VETUSDT", 1, 550, http_client, websocket_client)
    aave = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AAVEUSDT", 0.1, 550, http_client, websocket_client)
  elif pool == "4":
    grt = MACD_strategy({"name" : "30m", "ms" : 1800000}, "GRTUSDT", 1, 550, http_client, websocket_client)
    luna = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LUNAUSDT", 1, 550, http_client, websocket_client)
    bat = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BATUSDT", 0.1, 550, http_client, websocket_client)
    neo = MACD_strategy({"name" : "30m", "ms" : 1800000}, "NEOUSDT", 0.01, 550, http_client, websocket_client)
    qtum = MACD_strategy({"name" : "30m", "ms" : 1800000}, "QTUMUSDT", 0.1, 550, http_client, websocket_client)
    iost = MACD_strategy({"name" : "30m", "ms" : 1800000}, "IOSTUSDT", 1, 550, http_client, websocket_client)
    theta = MACD_strategy({"name" : "30m", "ms" : 1800000}, "THETAUSDT", 0.1, 550, http_client, websocket_client)
    algo = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ALGOUSDT", 0.1, 550, http_client, websocket_client)
    zil = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ZILUSDT", 1, 550, http_client, websocket_client)
    knc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "KNCUSDT", 1, 550, http_client, websocket_client)
  elif pool == "5":
    ogn = MACD_strategy({"name" : "30m", "ms" : 1800000}, "OGNUSDT", 1, 550, http_client, websocket_client)
    coti = MACD_strategy({"name" : "30m", "ms" : 1800000}, "COTIUSDT", 1, 550, http_client, websocket_client)
    ankr = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ANKRUSDT", 1, 550, http_client, websocket_client)
    zrx = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ZRXUSDT", 0.1, 550, http_client, websocket_client)
    comp = MACD_strategy({"name" : "30m", "ms" : 1800000}, "COMPUSDT", 0.001, 550, http_client, websocket_client)
    doge = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DOGEUSDT", 1, 550, http_client, websocket_client)
    kava = MACD_strategy({"name" : "30m", "ms" : 1800000}, "KAVAUSDT", 0.1, 550, http_client, websocket_client)
    band = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BANDUSDT", 0.1, 550, http_client, websocket_client)
    rlc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "RLCUSDT", 0.1, 550, http_client, websocket_client)
  elif pool == "6":
    waves = MACD_strategy({"name" : "30m", "ms" : 1800000}, "WAVESUSDT", 0.1, 550, http_client, websocket_client)
    snx = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SNXUSDT", 0.1, 550, http_client, websocket_client)
  #  defi = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DEFIUSDT", 0.001, 550, http_client, websocket_client)
    yfi = MACD_strategy({"name" : "30m", "ms" : 1800000}, "YFIUSDT", 0.001, 550, http_client, websocket_client)
    egld = MACD_strategy({"name" : "30m", "ms" : 1800000}, "EGLDUSDT", 0.1, 550, http_client, websocket_client)
    sol = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SOLUSDT", 1, 550, http_client, websocket_client)
    storj = MACD_strategy({"name" : "30m", "ms" : 1800000}, "STORJUSDT", 1, 550, http_client, websocket_client)
    fil = MACD_strategy({"name" : "30m", "ms" : 1800000}, "FILUSDT", 0.1, 550, http_client, websocket_client)
    matic = MACD_strategy({"name" : "30m", "ms" : 1800000}, "MATICUSDT", 1, 550, http_client, websocket_client)
