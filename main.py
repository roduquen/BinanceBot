from client.websocket_client import WebSocketClient
from client.http_client import HTTPClient
from array_class.array import Array
from binance_keys import *

http_client = HTTPClient(api_key_id, secret_key)
websocket_client = WebSocketClient(api_key_id, secret_key)

array_1m = Array("1m", "BTCUSDT", http_client, websocket_client)
