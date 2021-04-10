from client.websocket_client import WebSocketClient
from client.http_client import HTTPClient
from strategy.macd_strategy import MACD_strategy
from binance_keys import *
import time
import sys

http_client = HTTPClient(api_key_id, secret_key)
websocket_client = WebSocketClient(api_key_id, secret_key)
pool = sys.argv[1]

if pool == "1":
  btc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BTCUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  bch = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BCHUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  eth = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ETHUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  etc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ETCUSDT", 0.01, 550, http_client, websocket_client)
  time.sleep(60)
  ltc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LTCUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  xrp = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XRPUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  eos = MACD_strategy({"name" : "30m", "ms" : 1800000}, "EOSUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  ada = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ADAUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  avax = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AVAXUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  xlm = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XLMUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
elif pool == "2":
  trx = MACD_strategy({"name" : "30m", "ms" : 1800000}, "TRXUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  link = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LINKUSDT", 0.01, 550, http_client, websocket_client)
  time.sleep(60)
  bnb = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BNBUSDT", 0.01, 550, http_client, websocket_client)
  time.sleep(60)
  xmr = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XMRUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  dash = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DASHUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  zec = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ZECUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  xtz = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XTZUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  atom = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ATOMUSDT", 0.01, 550, http_client, websocket_client)
  time.sleep(60)
  ont = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ONTUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  enj = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ENJUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
elif pool == "3":
  axs = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AXSUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  chz = MACD_strategy({"name" : "30m", "ms" : 1800000}, "CHZUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  dot = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DOTUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  inch = MACD_strategy({"name" : "30m", "ms" : 1800000}, "1INCHUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  uni = MACD_strategy({"name" : "30m", "ms" : 1800000}, "UNIUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  sushi = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SUSHIUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  sxp = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SXPUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  iota = MACD_strategy({"name" : "30m", "ms" : 1800000}, "IOTAUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  vet = MACD_strategy({"name" : "30m", "ms" : 1800000}, "VETUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  aave = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AAVEUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
elif pool == "4":
  grt = MACD_strategy({"name" : "30m", "ms" : 1800000}, "GRTUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  luna = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LUNAUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  bat = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BATUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  neo = MACD_strategy({"name" : "30m", "ms" : 1800000}, "NEOUSDT", 0.01, 550, http_client, websocket_client)
  time.sleep(60)
  qtum = MACD_strategy({"name" : "30m", "ms" : 1800000}, "QTUMUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  iost = MACD_strategy({"name" : "30m", "ms" : 1800000}, "IOSTUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  theta = MACD_strategy({"name" : "30m", "ms" : 1800000}, "THETAUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  algo = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ALGOUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  zil = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ZILUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  knc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "KNCUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
elif pool == "5":
  ogn = MACD_strategy({"name" : "30m", "ms" : 1800000}, "OGNUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  coti = MACD_strategy({"name" : "30m", "ms" : 1800000}, "COTIUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  ankr = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ANKRUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  zrx = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ZRXUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  comp = MACD_strategy({"name" : "30m", "ms" : 1800000}, "COMPUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  omg = MACD_strategy({"name" : "30m", "ms" : 1800000}, "OMGUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  doge = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DOGEUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  kava = MACD_strategy({"name" : "30m", "ms" : 1800000}, "KAVAUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  band = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BANDUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  rlc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "RLCUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
elif pool == "6":
  waves = MACD_strategy({"name" : "30m", "ms" : 1800000}, "WAVESUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  mkr = MACD_strategy({"name" : "30m", "ms" : 1800000}, "MKRUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  snx = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SNXUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  defi = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DEFIUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  yfi = MACD_strategy({"name" : "30m", "ms" : 1800000}, "YFIUSDT", 0.001, 550, http_client, websocket_client)
  time.sleep(60)
  egld = MACD_strategy({"name" : "30m", "ms" : 1800000}, "EGLDUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  sol = MACD_strategy({"name" : "30m", "ms" : 1800000}, "SOLUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  storj = MACD_strategy({"name" : "30m", "ms" : 1800000}, "STORJUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
  fil = MACD_strategy({"name" : "30m", "ms" : 1800000}, "FILUSDT", 0.1, 550, http_client, websocket_client)
  time.sleep(60)
  matic = MACD_strategy({"name" : "30m", "ms" : 1800000}, "MATICUSDT", 1, 550, http_client, websocket_client)
  time.sleep(60)
