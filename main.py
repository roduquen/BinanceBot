from client.websocket_client import WebSocketClient
from client.http_client import HTTPClient
from strategy.macd_strategy import MACD_strategy
from binance_keys import *

http_client = HTTPClient(api_key_id, secret_key)
websocket_client = WebSocketClient(api_key_id, secret_key)

btc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BTCUSDT", 0.001, 300, http_client, websocket_client)
bch = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BCHUSDT", 0.001, 300, http_client, websocket_client)
eth = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ETHUSDT", 0.001, 300, http_client, websocket_client)
etc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ETCUSDT", 0.01, 300, http_client, websocket_client)
ltc = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LTCUSDT", 0.001, 300, http_client, websocket_client)
xrp = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XRPUSDT", 0.1, 300, http_client, websocket_client)
eos = MACD_strategy({"name" : "30m", "ms" : 1800000}, "EOSUSDT", 0.1, 300, http_client, websocket_client)
ada = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ADAUSDT", 1, 300, http_client, websocket_client)
avax = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AVAXUSDT", 1, 300, http_client, websocket_client)
xlm = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XLMUSDT", 1, 300, http_client, websocket_client)
trx = MACD_strategy({"name" : "30m", "ms" : 1800000}, "TRXUSDT", 1, 300, http_client, websocket_client)
link = MACD_strategy({"name" : "30m", "ms" : 1800000}, "LINKUSDT", 0.01, 300, http_client, websocket_client)
xmr = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XMRUSDT", 0.001, 300, http_client, websocket_client)
dash = MACD_strategy({"name" : "30m", "ms" : 1800000}, "DASHUSDT", 0.001, 300, http_client, websocket_client)
zec = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ZECUSDT", 0.001, 300, http_client, websocket_client)
xtz = MACD_strategy({"name" : "30m", "ms" : 1800000}, "XTZUSDT", 0.1, 300, http_client, websocket_client)
bnb = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BNBUSDT", 0.01, 300, http_client, websocket_client)
atom = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ATOMUSDT", 0.01, 300, http_client, websocket_client)
ont = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ONTUSDT", 0.1, 300, http_client, websocket_client)
enj = MACD_strategy({"name" : "30m", "ms" : 1800000}, "ENJUSDT", 1, 300, http_client, websocket_client)
axs = MACD_strategy({"name" : "30m", "ms" : 1800000}, "AXSUSDT", 1, 300, http_client, websocket_client)
chz = MACD_strategy({"name" : "30m", "ms" : 1800000}, "CHZUSDT", 1, 300, http_client, websocket_client)
