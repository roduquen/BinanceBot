from client.websocket_client import WebSocketClient
from client.http_client import HTTPClient
from strategy.macd_strategy import MACD_strategy
from binance_keys import *

http_client = HTTPClient(api_key_id, secret_key)
websocket_client = WebSocketClient(api_key_id, secret_key)

macd_strat = MACD_strategy({"name" : "30m", "ms" : 1800000}, "BTCUSDT", 0.001, 100, http_client, websocket_client)
